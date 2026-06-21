import json
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from astra.curiosity.engine import research_topic_loop
from astra.curiosity.wiki_research import get_related_topics, get_summary

DOMAINS_FILE = "data/domains.json"


def load_domain_names():

    try:
        with open(DOMAINS_FILE, "r", encoding="utf-8") as file:
            domains = json.load(file)

        names = sorted(domains.keys())

        if names:
            return names

    except (OSError, json.JSONDecodeError):
        pass

    return ["programming"]


class ResearchGui:

    def __init__(self, root):
        self.root = root
        self.root.title("Astra Research")
        self.root.geometry("780x560")

        self.domain_names = load_domain_names()
        self.topic_var = tk.StringVar()
        self.domain_var = tk.StringVar(
            value=(
                "programming"
                if "programming" in self.domain_names
                else self.domain_names[0]
            )
        )
        self.reset_var = tk.BooleanVar(value=False)
        self.max_topics_var = tk.IntVar(value=10)
        self.delay_var = tk.IntVar(value=2)
        self.stop_requested = False

        self._build_layout()

    def _build_layout(self):
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Research Topic").grid(
            row=0,
            column=0,
            sticky="w"
        )

        topic_entry = ttk.Entry(
            frame,
            textvariable=self.topic_var
        )
        topic_entry.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(4, 12)
        )
        topic_entry.focus()

        ttk.Label(frame, text="Domain").grid(
            row=2,
            column=0,
            sticky="w"
        )

        ttk.Combobox(
            frame,
            textvariable=self.domain_var,
            values=self.domain_names,
            width=28,
            state="readonly"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=(4, 12)
        )

        ttk.Checkbutton(
            frame,
            text="Reset queue and visited topics before research",
            variable=self.reset_var
        ).grid(
            row=3,
            column=1,
            columnspan=2,
            sticky="w",
            pady=(4, 12)
        )

        ttk.Label(frame, text="Max Topics").grid(
            row=4,
            column=0,
            sticky="w"
        )

        ttk.Spinbox(
            frame,
            from_=1,
            to=500,
            textvariable=self.max_topics_var,
            width=8
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=(4, 12)
        )

        ttk.Label(frame, text="Delay Seconds").grid(
            row=4,
            column=1,
            sticky="w"
        )

        ttk.Spinbox(
            frame,
            from_=0,
            to=60,
            textvariable=self.delay_var,
            width=8
        ).grid(
            row=5,
            column=1,
            sticky="e",
            pady=(4, 12)
        )

        self.research_button = ttk.Button(
            frame,
            text="Start Learning Loop",
            command=self.start_research
        )
        self.research_button.grid(
            row=5,
            column=2,
            sticky="w",
            pady=(4, 12)
        )

        self.stop_button = ttk.Button(
            frame,
            text="Stop",
            command=self.stop_research,
            state="disabled"
        )
        self.stop_button.grid(
            row=6,
            column=2,
            sticky="w",
            pady=(0, 12)
        )

        self.status_label = ttk.Label(frame, text="Ready.")
        self.status_label.grid(
            row=6,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(0, 12)
        )

        ttk.Label(frame, text="Research Log").grid(
            row=7,
            column=0,
            sticky="w"
        )

        self.output = tk.Text(
            frame,
            wrap="word",
            height=18
        )
        self.output.grid(
            row=8,
            column=0,
            columnspan=3,
            sticky="nsew"
        )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.output.yview
        )
        scrollbar.grid(
            row=8,
            column=3,
            sticky="ns"
        )
        self.output.configure(yscrollcommand=scrollbar.set)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.rowconfigure(8, weight=1)

    def start_research(self):
        topic = self.topic_var.get().strip()

        if not topic:
            messagebox.showwarning(
                "Missing topic",
                "Enter a topic for Astra to research."
            )
            return

        self.research_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.stop_requested = False
        self.status_label.configure(text="Learning related topics...")
        self.output.delete("1.0", "end")

        worker = threading.Thread(
            target=self._research,
            args=(topic,),
            daemon=True
        )
        worker.start()

    def stop_research(self):
        self.stop_requested = True
        self.status_label.configure(text="Stopping after current topic...")

    def _research(self, topic):
        try:
            result = research_topic_loop(
                topic=topic,
                get_summary=get_summary,
                get_related_topics=get_related_topics,
                domain=self.domain_var.get().strip() or "programming",
                reset=self.reset_var.get(),
                max_topics=max(
                    1,
                    self.max_topics_var.get()
                ),
                delay_seconds=max(
                    0,
                    self.delay_var.get()
                ),
                progress_callback=self._queue_progress,
                should_stop=lambda: self.stop_requested
            )
        except Exception as error:
            self.root.after(
                0,
                self._show_error,
                str(error)
            )
            return

        self.root.after(
            0,
            self._show_complete,
            result
        )

    def _queue_progress(self, result, processed):
        self.root.after(
            0,
            self._show_progress,
            result,
            processed
        )

    def _show_progress(self, result, processed):
        self.status_label.configure(
            text=f"Checked {processed}: {result['topic']}"
        )

        if result["saved"]:
            text = (
                f"[{processed}] {result['topic']}\n"
                f"Saved: True\n"
                f"Related topics: {len(result['related'])}\n"
                f"Accepted into queue: {result['accepted']}\n"
                f"Rejected: {result['rejected']}\n"
                f"Keywords: {', '.join(result.get('keywords', []))}\n"
                "\n"
            )
        else:
            text = (
                f"[{processed}] {result['topic']}\n"
                f"Skipped: {result['message']}\n\n"
            )

        self.output.insert("end", text)
        self.output.see("end")

    def _show_complete(self, result):
        self.research_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(
            text=(
                f"{result['message']} "
                f"Queue left: {result['remaining_queue']}."
            )
        )

    def _show_error(self, message):
        self.research_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="Research failed.")
        messagebox.showerror(
            "Research failed",
            message
        )


def main():
    root = tk.Tk()
    ResearchGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()

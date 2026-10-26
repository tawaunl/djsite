// Mobile nav, booking form submit, and press-kit helpers.

(() => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    nav.addEventListener("click", (ev) => {
      if (ev.target.closest("a")) {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  // ------------------------------------------------------------ booking form
  const form = document.querySelector(".booking-form");
  if (form) {
    const status = form.querySelector(".form-status");
    const button = form.querySelector("button[type=submit]");
    const dateInput = form.querySelector("[name=event_date]");
    if (dateInput) dateInput.min = new Date().toISOString().slice(0, 10);

    const setStatus = (text, kind) => {
      status.textContent = text;
      status.className = "form-status" + (kind ? " " + kind : "");
    };

    const validate = () => {
      let firstBad = null;
      form.querySelectorAll("[required]").forEach((el) => {
        const bad = !el.checkValidity();
        el.setAttribute("aria-invalid", String(bad));
        if (bad && !firstBad) firstBad = el;
      });
      if (firstBad) firstBad.focus();
      return !firstBad;
    };

    const summary = (data) => {
      const labels = {
        name: "Name", email: "Email", event_date: "Event date", event_type: "Event type",
        venue: "Venue / city", guests: "Expected guests", set_length: "Set length",
        budget: "Budget", message: "Details",
      };
      return Object.entries(labels)
        .filter(([key]) => data.get(key))
        .map(([key, label]) => `${label}: ${data.get(key)}`)
        .join("\n");
    };

    form.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      if (!validate()) {
        setStatus("Fill in the highlighted fields.", "err");
        return;
      }
      const data = new FormData(form);
      if (data.get("company")) return; // honeypot: bots fill hidden fields

      const subject = `Booking request: ${data.get("event_type")} on ${data.get("event_date")}`;
      const endpoint = form.dataset.endpoint;

      if (!endpoint) {
        const href = `mailto:${form.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(summary(data))}`;
        window.location.href = href;
        setStatus("Your email app should open with the request filled in. Hit send there.", "ok");
        return;
      }

      button.disabled = true;
      setStatus("Sending...");
      data.delete("company");
      data.append("_subject", subject);
      try {
        const res = await fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } });
        if (!res.ok) throw new Error(String(res.status));
        form.reset();
        setStatus("Request sent. You'll hear back soon.", "ok");
      } catch {
        setStatus(`That didn't go through. Email ${form.dataset.email} directly.`, "err");
      } finally {
        button.disabled = false;
      }
    });

    form.addEventListener("input", (ev) => {
      if (ev.target.getAttribute("aria-invalid") === "true" && ev.target.checkValidity()) {
        ev.target.setAttribute("aria-invalid", "false");
      }
    });
  }

  // ---------------------------------------------------------- press helpers
  document.querySelectorAll("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const target = document.getElementById(btn.dataset.copy);
      if (!target) return;
      try {
        await navigator.clipboard.writeText(target.innerText.trim());
        const label = btn.textContent;
        btn.textContent = "Copied";
        setTimeout(() => (btn.textContent = label), 1500);
      } catch {
        window.getSelection().selectAllChildren(target);
      }
    });
  });

  document.querySelectorAll("[data-print]").forEach((btn) => btn.addEventListener("click", () => window.print()));
})();

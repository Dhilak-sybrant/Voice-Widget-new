<script>
(function() {
    const agentId = document.currentScript.dataset.agent || "agent_01jwnymxeaeg29wjmdm16pmf89";

    const widget = document.createElement("elevenlabs-convai");
    widget.setAttribute("agent-id", agentId);

    const elevenScript = document.createElement("script");
    elevenScript.src = "https://elevenlabs.io/convai-widget/index.js";
    elevenScript.type = "text/javascript";
    elevenScript.async = true;

    document.body.appendChild(widget);
    document.body.appendChild(elevenScript);

    const checkInterval = setInterval(() => {
        const shadowRoot = widget.shadowRoot || widget.attachShadow?.();
        if (!shadowRoot) return;

        const brandingEl = shadowRoot.querySelector('[class*="poweredBy"], div[part="branding"]');
        if (brandingEl) {
            brandingEl.textContent = "Powered by Sybrant";
            clearInterval(checkInterval);
        }
    }, 300);
})();
</script>

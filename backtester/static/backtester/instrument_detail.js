  function cloneTemplateInto(templateId, targetId, rewrites) {
    const tmpl = document.querySelector(`#${templateId}`);
    if (!tmpl) return;
    const target = document.querySelector(`#${targetId}`);
    if (!target) return;
    target.innerText = '';
    const clone = tmpl.content.cloneNode(true);
    if (rewrites) {
      const script = clone.querySelector('script');
      script.textContent = rewrites(script.textContent);
    }
    target.appendChild(clone);
  }
  function setSymbol(scriptContent) {
    return scriptContent.replace(/"symbol": "([^"]*)"/g, () => {
      return `"symbol": "${symbol}"`;
    });
  }
  cloneTemplateInto('symbol-info-template', 'symbol-info', setSymbol);
  cloneTemplateInto('advanced-chart-template', 'advanced-chart');
  cloneTemplateInto('company-profile-template', 'company-profile', setSymbol);
  cloneTemplateInto('fundamental-data-template', 'fundamental-data', setSymbol);
  cloneTemplateInto('technical-analysis-template', 'technical-analysis', setSymbol);
  cloneTemplateInto('top-stories-template', 'top-stories', setSymbol);
  if (symbol) {
    document.title = `Stock Details - ${symbol}`;
  }
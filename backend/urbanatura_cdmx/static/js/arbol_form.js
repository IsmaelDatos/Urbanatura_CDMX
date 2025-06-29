const alturaInput = document.getElementById('altura');
if (alturaInput && parseFloat(alturaInput.value) > 50) {
  alert("La altura no puede ser mayor a 50 metros.");
  return;
}
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('arbolForm');
    if (!form) return;
    if (form._hasSubmitListener) return;
    form._hasSubmitListener = true;
    let isSubmitting = false;
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (isSubmitting) return;
        isSubmitting = true;
        const submitButton = form.querySelector('button[type="submit"]');
        const originalHTML = submitButton.innerHTML;
        try {
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
            const resp = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await resp.json();
            if (!data.success) {
              const errorMsg = data.error || 
                (data.errors ? Object.values(data.errors).flat().join('\n') : 'Error al procesar el formulario');
              throw new Error(errorMsg);
            }
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
                return;
            }
        } catch (err) {
            alert(err.message);
            console.error('Error:', err);
        } finally {
            isSubmitting = false;
            submitButton.disabled = false;
            submitButton.innerHTML = originalHTML;
        }
    });
}); 
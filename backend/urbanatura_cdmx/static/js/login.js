function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(loginForm);
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        document.querySelectorAll('.error-message').forEach(el => {
            el.classList.add('hidden');
            el.textContent = '';
        });
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Verificando...';
        submitBtn.disabled = true;
        try {
            const response = await fetch(loginForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                submitBtn.innerHTML = '<i class="fas fa-check mr-2"></i> ¡Bienvenido!';
                submitBtn.classList.replace('from-green-600', 'bg-green-500');
                submitBtn.classList.remove('to-green-700', 'hover:from-green-700', 'hover:to-green-800');
                setTimeout(() => {
                    window.location.href = data.redirect_url || "/";
                }, 1000);
            } else {
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
                if (data.errors) {
                    handleFormErrors(data.errors);
                } else {
                    showFlashMessage(data.error || 'Credenciales inválidas');
                }
            }
        } catch (error) {
            console.error('Error:', error);
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
            showFlashMessage('Error al conectar con el servidor');
        }
    });
    function handleFormErrors(errors) {
        for (const [field, error] of Object.entries(errors)) {
            const errorElement = document.getElementById(`${field}-error`);
            if (errorElement) {
                errorElement.textContent = error;
                errorElement.classList.remove('hidden');
                const input = loginForm.querySelector(`[name="${field}"]`);
                input.classList.add('border-red-500', 'animate-shake');
                setTimeout(() => {
                    input.classList.remove('border-red-500', 'animate-shake');
                }, 3000);
            }
        }
    }
    function showFlashMessage(message) {
        const flashElement = document.createElement('div');
        flashElement.className = 'flash-message bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4 rounded animate-fade-in';
        flashElement.innerHTML = `<p>${message}</p>`;
        
        loginForm.insertBefore(flashElement, loginForm.firstChild);
        setTimeout(() => {
            flashElement.classList.add('animate-fade-out');
            setTimeout(() => flashElement.remove(), 300);
        }, 5000);
    }
}

document.addEventListener('DOMContentLoaded', setupLoginForm);
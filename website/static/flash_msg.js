function dismissFlashMessage(event) {
    const msg = event.target.closest('.flash-message');
    msg.style.opacity = '0'
    setTimeout(() => msg.remove(), 3000);
}
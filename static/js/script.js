document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".alert").forEach((el) => {
    setTimeout(() => {
      const alert = bootstrap.Alert.getOrCreateInstance(el);
      alert.close();
    }, 4000);
  });
});

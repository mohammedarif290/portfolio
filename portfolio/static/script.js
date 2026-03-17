document.getElementById("contactForm").addEventListener("submit", function(e) {

  var name = document.getElementById("name").value;
  var email = document.getElementById("email").value;

  if (name === "" || email === "") {
    e.preventDefault();
    document.getElementById("msg").innerText = "❌ Please fill required fields";
    return;
  }

  document.getElementById("msg").innerText = "⏳ Sending...";
});
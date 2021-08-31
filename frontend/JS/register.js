function reg() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  let email = document.getElementById("email").value;
  console.log(username, password, email);
  fetch("https://fast-bayou-16865.herokuapp.com/register/", {
    method: "POST",
    body: JSON.stringify({
      username: username,
      password: password,
      email: email,
    }),

    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  })
    .then((response) => response.json())
    .then((json) => console.log(json));
}

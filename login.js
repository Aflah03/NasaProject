// Toggle between login and registration forms
function toggleForm() {
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  loginForm.classList.toggle('hidden');
  registerForm.classList.toggle('hidden');
}

// Function to save a user to localStorage
function saveUserToLocalStorage(user) {
  let users = JSON.parse(localStorage.getItem('users')) || [];
  users.push(user);
  localStorage.setItem('users', JSON.stringify(users));
}

// Function to retrieve users from localStorage
function getUsersFromLocalStorage() {
  return JSON.parse(localStorage.getItem('users')) || [];
}

// Event listener for the registration form
document.getElementById('submitRegister').addEventListener('click', function (event) {
  event.preventDefault();

  const name = document.getElementById('rName').value;
  const email = document.getElementById('rEmailReg').value;
  const password = document.getElementById('rPasswordReg').value;
  const confirmPassword = document.getElementById('rConfirmPassword').value;

  if (password !== confirmPassword) {
    alert('Passwords do not match!');
    return;
  }

  // Retrieve users from localStorage
  const users = getUsersFromLocalStorage();

  // Check if the email is already registered
  const userExists = users.some(user => user.email === email);

  if (userExists) {
    alert('User with this email already exists!');
  } else {
    // Save the new user to localStorage
    const newUser = { name, email, password };
    saveUserToLocalStorage(newUser);
    alert('Registration successful! You can now log in.');
    toggleForm(); // Switch back to login form
  }
});

// Event listener for the login form
document.getElementById('submitsignUp').addEventListener('click', function (event) {
  event.preventDefault();

  const email = document.getElementById('rEmail').value;
  const password = document.getElementById('rPassword').value;

  // Retrieve users from localStorage
  const users = getUsersFromLocalStorage();

  // Check if the entered email and password match any registered user
  const user = users.find(user => user.email === email && user.password === password);

  if (user) {
      //redirect to community on succesful login
    window.location.href = 'home.html';
  } else {
    alert('Incorrect email or password!');
  }
});


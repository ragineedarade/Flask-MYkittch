// static/script.js - Consolidated and Corrected

document.addEventListener("DOMContentLoaded", () => {
  // --- Firebase Client-Side SDK Initialization (if not already in HTML) ---
  // If you've put the firebaseConfig and firebase.initializeApp() directly in your HTML files
  // before this script, you can remove this block. Otherwise, keep it.
  // Make sure to replace placeholders with your actual Firebase project config.
  // const firebaseConfig = {
  //     apiKey: "YOUR_API_KEY",
  //     authDomain: "YOUR_AUTH_DOMAIN",
  //     projectId: "YOUR_PROJECT_ID",
  //     storageBucket: "YOUR_STORAGE_BUCKET",
  //     messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  //     appId: "YOUR_APP_ID"
  // };
  // if (!firebase.apps.length) {
  //     firebase.initializeApp(firebaseConfig);
  // }
  // const auth = firebase.auth();
  // const db = firebase.firestore(); // For client-side Firestore if needed
  // const storage = firebase.storage(); // For client-side Storage if needed
  // --- End Firebase Client-Side SDK Initialization ---

  // --- Mobile Navigation Toggle ---
  const hamburger = document.querySelector(".hamburger");
  const navLinks = document.querySelector(".nav-links");

  if (hamburger && navLinks) {
    hamburger.addEventListener("click", () => {
      navLinks.classList.toggle("active");
    });
  }

  // --- "What Can I Cook?" Overlay Toggle ---
  const whatCanICookBtn = document.getElementById("whatCanICookBtn");
  const ingredientSearchOverlay = document.getElementById(
    "ingredientSearchOverlay"
  );

  if (whatCanICookBtn && ingredientSearchOverlay) {
    whatCanICookBtn.addEventListener("click", (e) => {
      e.preventDefault(); // Prevent default link behavior
      ingredientSearchOverlay.style.display = "flex";
    });

    // Close overlay if clicked outside search-box (or on close button)
    ingredientSearchOverlay.addEventListener("click", (e) => {
      if (e.target === ingredientSearchOverlay) {
        ingredientSearchOverlay.style.display = "none";
      }
    });
  }

  // --- Add/Remove Ingredients on Submit Recipe Page ---
  const ingredientsContainer = document.getElementById("ingredientsContainer");
  if (ingredientsContainer) {
    const addIngredientBtn = ingredientsContainer.querySelector(
      ".btn-add-ingredient"
    );

    // Function to add a new ingredient input group
    const addIngredientInputGroup = () => {
      const newIngredientGroup = document.createElement("div");
      newIngredientGroup.classList.add("ingredient-input-group");
      newIngredientGroup.innerHTML = `
                <input type="text" name="ingredientQuantity[]" placeholder="Quantity (e.g., 2 cups)" class="ingredient-quantity">
                <input type="text" name="ingredientItem[]" placeholder="Item (e.g., flour)" class="ingredient-item">
                <button type="button" class="btn-remove-ingredient"><i class="fas fa-minus-circle"></i></button>
            `;
      ingredientsContainer.insertBefore(newIngredientGroup, addIngredientBtn);
    };

    // Add initial empty ingredient input if there's none
    if (
      ingredientsContainer.querySelectorAll(".ingredient-input-group")
        .length === 0
    ) {
      addIngredientInputGroup();
    }

    // Event listener for adding ingredients
    addIngredientBtn.addEventListener("click", addIngredientInputGroup);

    // Event listener for removing ingredients (delegated)
    ingredientsContainer.addEventListener("click", (e) => {
      if (e.target.closest(".btn-remove-ingredient")) {
        const group = e.target.closest(".ingredient-input-group");
        // Ensure at least one ingredient input remains
        if (
          ingredientsContainer.querySelectorAll(".ingredient-input-group")
            .length > 1
        ) {
          group.remove();
        } else {
          alert("You must have at least one ingredient.");
        }
      }
    });

    // --- Handle Recipe Submission (Connect to Flask Backend) ---
    const recipeSubmissionForm = document.getElementById(
      "recipeSubmissionForm"
    );
    if (recipeSubmissionForm) {
      recipeSubmissionForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent default form submission

        // 1. Get Firebase ID Token
        const user = auth.currentUser; // 'auth' comes from Firebase SDK initialization
        if (!user) {
          alert("You must be logged in to submit a recipe.");
          return;
        }
        let idToken;
        try {
          idToken = await user.getIdToken();
        } catch (error) {
          console.error("Error getting Firebase ID token:", error);
          alert(
            "Failed to get authentication token. Please try logging in again."
          );
          return;
        }

        // 2. Collect form data
        const formData = new FormData(recipeSubmissionForm);

        // 3. Send data to Flask backend
        try {
          const response = await fetch("/submit-recipe", {
            method: "POST",
            body: formData, // FormData automatically sets Content-Type to multipart/form-data
            headers: {
              Authorization: `Bearer ${idToken}`, // Send the ID token for backend verification
            },
          });

          const result = await response.json();

          if (response.ok) {
            alert(result.message);
            recipeSubmissionForm.reset(); // Clear the form
            // Optionally redirect to the recipes page or a confirmation page
            window.location.href = "/recipes";
          } else {
            alert(
              "Error: " +
                (result.error || "Something went wrong on the server.")
            );
          }
        } catch (error) {
          console.error("Submission error:", error);
          alert(
            "An unexpected error occurred. Please check your network and try again."
          );
        }
      });
    }
  } // End of if (ingredientsContainer)

  // --- Star Rating on Recipe Detail Page ---
  const starRatingInputs = document.querySelectorAll(".star-rating-input i");
  if (starRatingInputs.length > 0) {
    starRatingInputs.forEach((star) => {
      star.addEventListener("click", () => {
        const value = parseInt(star.dataset.value);
        starRatingInputs.forEach((s) => {
          if (parseInt(s.dataset.value) <= value) {
            s.classList.add("fas");
            s.classList.remove("far");
          } else {
            s.classList.remove("fas");
            s.classList.add("far");
          }
        });
      });

      star.addEventListener("mouseover", () => {
        const value = parseInt(star.dataset.value);
        starRatingInputs.forEach((s) => {
          if (parseInt(s.dataset.value) <= value) {
            s.classList.add("fas");
            s.classList.remove("far");
          } else {
            s.classList.remove("fas");
            s.classList.add("far");
          }
        });
      });

      star.addEventListener("mouseout", () => {
        // Reset to current selected rating (or clear if none selected)
        // For this demo, just clear it on mouseout if no persistent state
        const currentRating = document.querySelector(
          ".star-rating-input i.fas"
        );
        if (!currentRating) {
          // If no star is actively selected
          starRatingInputs.forEach((s) => {
            s.classList.remove("fas");
            s.classList.add("far");
          });
        }
      });
    });
  }

  // --- Basic Drag & Drop for Meal Planner (Conceptual - now with backend interaction) ---
  const recipePlaceholders = document.querySelectorAll(".recipe-placeholder");
  const dayCells = document.querySelectorAll(".day-cell");

  if (recipePlaceholders.length > 0 && dayCells.length > 0) {
    recipePlaceholders.forEach((placeholder) => {
      placeholder.setAttribute("draggable", true);
      placeholder.addEventListener("dragstart", (e) => {
        e.dataTransfer.setData(
          "text/plain",
          e.target.textContent.replace("(Drag me!)", "").trim()
        ); // Pass only recipe text
        e.target.classList.add("dragging");
      });
      placeholder.addEventListener("dragend", (e) => {
        e.target.classList.remove("dragging");
      });
    });

    dayCells.forEach((cell) => {
      cell.addEventListener("dragover", (e) => {
        e.preventDefault(); // Allow drop
        cell.classList.add("drag-over");
      });
      cell.addEventListener("dragleave", (e) => {
        cell.classList.remove("drag-over");
      });
      cell.addEventListener("drop", async (e) => {
        e.preventDefault();
        cell.classList.remove("drag-over");
        const recipeText = e.dataTransfer.getData("text/plain");
        const date =
          cell.dataset.date || new Date().toISOString().split("T")[0]; // Get date from cell or current date
        const mealType = cell.dataset.mealType || "Dinner"; // Get meal type from cell or default

        // 1. Get Firebase ID Token
        const user = auth.currentUser;
        if (!user) {
          alert("You must be logged in to save meal plans.");
          return;
        }
        let idToken;
        try {
          idToken = await user.getIdToken();
        } catch (error) {
          console.error("Error getting Firebase ID token:", error);
          alert(
            "Failed to get authentication token. Please try logging in again."
          );
          return;
        }

        // 2. Send data to backend
        try {
          const response = await fetch("/save_meal", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${idToken}`,
            },
            body: JSON.stringify({
              date: date,
              meal_type: mealType,
              recipe_text: recipeText,
            }),
          });

          const result = await response.json();

          if (response.ok) {
            const newMealSlot = document.createElement("div");
            newMealSlot.classList.add("meal-slot");
            newMealSlot.textContent = `${mealType}: ${recipeText}`;
            cell.appendChild(newMealSlot);
            alert(result.message);
            // Optionally, re-fetch meal plans to update the view
            // fetchAndDisplayMealPlans();
          } else {
            alert(
              `Error saving meal: ${result.reason || "Something went wrong."}`
            );
          }
        } catch (error) {
          console.error("Error saving meal plan:", error);
          alert("Failed to save meal plan. Please try again.");
        }
      });
    });
  }

  // --- Login/Sign Up Tabs and Form Switching (for login.html/signup.html) ---
  const tabButtons = document.querySelectorAll(".auth-tabs .tab-btn");
  const authForms = document.querySelectorAll(".auth-form");

  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const targetTab = button.dataset.tab;

      // Deactivate all tabs and forms
      tabButtons.forEach((btn) => btn.classList.remove("active"));
      authForms.forEach((form) => form.classList.remove("active"));

      // Activate the clicked tab
      button.classList.add("active");

      // Activate the corresponding form
      const targetForm = document.getElementById(`${targetTab}-form`);
      if (targetForm) {
        targetForm.classList.add("active");
      }
    });
  });

  // Handle switch links within forms
  const switchLinks = document.querySelectorAll(
    ".auth-switch-text .switch-link"
  );
  switchLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault(); // Prevent default link behavior
      const targetTab = link.dataset.tab;

      // Find and click the corresponding tab button
      const targetButton = document.querySelector(
        `.auth-tabs .tab-btn[data-tab="${targetTab}"]`
      );
      if (targetButton) {
        targetButton.click();
      }
    });
  });

  // --- Handle Login Form Submission (Connect to Firebase Auth) ---
  const loginForm = document.getElementById("login-form"); // Assuming your login form has this ID
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("login-email").value;
      const password = document.getElementById("login-password").value;

      if (!email || !password) {
        alert("Please enter both email and password.");
        return;
      }

      try {
        // Use Firebase client-side SDK for login
        await auth.signInWithEmailAndPassword(email, password);
        alert("Login successful!");
        window.location.href = "/my-account.html"; // Redirect on success
      } catch (error) {
        console.error("Login error:", error.code, error.message);
        alert(`Login failed: ${error.message}`);
      }
    });
  }

  // --- Handle Sign Up Form Submission (Connect to Firebase Auth) ---
  const signupForm = document.getElementById("signup-form"); // Assuming your signup form has this ID
  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = document.getElementById("signup-username").value; // You might want to store this in Firestore later
      const email = document.getElementById("signup-email").value;
      const password = document.getElementById("signup-password").value;
      const confirmPassword = document.getElementById(
        "signup-confirm-password"
      ).value;

      if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
      }
      if (!username || !email || !password) {
        alert("Please fill in all sign up fields.");
        return;
      }

      try {
        // Use Firebase client-side SDK for sign up
        const userCredential = await auth.createUserWithEmailAndPassword(
          email,
          password
        );
        const user = userCredential.user;

        // Optionally, save additional user info (like username) to Firestore
        await db.collection("users").doc(user.uid).set({
          displayName: username,
          email: email,
          createdAt: firebase.firestore.FieldValue.serverTimestamp(),
        });

        alert("Sign Up successful! You are now logged in.");
        window.location.href = "/my-account.html"; // Redirect on success
      } catch (error) {
        console.error("Sign Up error:", error.code, error.message);
        alert(`Sign Up failed: ${error.message}`);
      }
    });
  }

  // --- Logic for recipes.html (dynamic loading) ---
  const recipeGrid = document.querySelector(".recipe-grid");
  // Only fetch recipes if on the recipes page
  if (recipeGrid && window.location.pathname === "/recipes") {
    fetchAndDisplayRecipes();
  }

  async function fetchAndDisplayRecipes() {
    try {
      const response = await fetch("/api/recipes"); // Fetch from your API endpoint
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const recipes = await response.json();

      if (recipeGrid) {
        recipeGrid.innerHTML = ""; // Clear existing placeholder recipes
        if (recipes.length === 0) {
          recipeGrid.innerHTML =
            "<p>No recipes found. Be the first to share one!</p>";
        } else {
          recipes.forEach((recipe) => {
            const recipeCard = document.createElement("div");
            recipeCard.classList.add("recipe-card");
            recipeCard.innerHTML = `
                            <img src="${
                              recipe.image_url ||
                              "https://via.placeholder.com/300x200?text=No+Image"
                            }" alt="${recipe.title}" />
                            <h3>${recipe.title}</h3>
                            <div class="rating">★★★★☆</div>
                            <p>${recipe.cuisine || ""} ${
              recipe.category ? `(${recipe.category})` : ""
            }</p>
                            <a href="/recipes/${
                              recipe.id
                            }" class="btn-small">View Recipe</a>
                        `;
            recipeGrid.appendChild(recipeCard);
          });
        }
      }
    } catch (error) {
      console.error("Error fetching recipes:", error);
      if (recipeGrid) {
        recipeGrid.innerHTML =
          "<p>Failed to load recipes. Please try again later.</p>";
      }
    }
  }

  // --- Logic for fetching and displaying meal plans (on meal-planner.html) ---
  const mealPlanGrid = document.querySelector(".meal-plan-grid"); // Assuming you have a grid for meal plans
  if (mealPlanGrid && window.location.pathname === "/meal-planner.html") {
    // Adjust path if different
    fetchAndDisplayMealPlans();
  }

  async function fetchAndDisplayMealPlans() {
    // 1. Get Firebase ID Token
    const user = auth.currentUser;
    if (!user) {
      mealPlanGrid.innerHTML = "<p>Please log in to view your meal plans.</p>";
      return;
    }
    let idToken;
    try {
      idToken = await user.getIdToken();
    } catch (error) {
      console.error("Error getting Firebase ID token:", error);
      mealPlanGrid.innerHTML =
        "<p>Failed to load meal plans. Please try logging in again.</p>";
      return;
    }

    try {
      const response = await fetch("/get_meal_plans", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${idToken}`,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const mealPlans = await response.json();
      mealPlanGrid.innerHTML = ""; // Clear existing content

      if (mealPlans.length === 0) {
        mealPlanGrid.innerHTML = "<p>No meal plans saved yet.</p>";
        return;
      }

      // Group meal plans by date or display simply
      // For simplicity, let's just list them
      mealPlans.forEach((plan) => {
        const mealPlanItem = document.createElement("div");
        mealPlanItem.classList.add("meal-plan-item"); // Add a class for styling
        mealPlanItem.innerHTML = `
                    <h4>${plan.date} - ${plan.meal_type}</h4>
                    <p>${plan.recipe_text}</p>
                    <small>User ID: ${plan.user_id}</small>
                `;
        mealPlanGrid.appendChild(mealPlanItem);
      });
    } catch (error) {
      console.error("Error fetching meal plans:", error);
      mealPlanGrid.innerHTML =
        "<p>Failed to load meal plans. Please try again later.</p>";
    }
  }

  // --- Authentication State Listener (Optional but Recommended) ---
  // This allows you to update UI elements based on login status
  auth.onAuthStateChanged((user) => {
    const loginSignUpBtn = document.querySelector('a.btn-primary[href="#"]'); // Assuming this is your login/signup button
    const myAccountLink = document.querySelector('a[href="my-account.html"]');

    if (user) {
      // User is signed in
      console.log("User is logged in:", user.uid);
      if (loginSignUpBtn) {
        loginSignUpBtn.textContent = "Logout";
        loginSignUpBtn.href = "#"; // Will handle logout via JS
        loginSignUpBtn.addEventListener(
          "click",
          async (e) => {
            e.preventDefault();
            try {
              await auth.signOut();
              alert("Logged out successfully!");
              window.location.href = "/"; // Redirect to home or login page
            } catch (error) {
              console.error("Logout error:", error);
              alert("Failed to log out.");
            }
          },
          { once: true }
        ); // Ensure event listener is added only once
      }
      if (myAccountLink) {
        myAccountLink.style.display = "block"; // Show "My Account"
      }
      // You might want to refresh meal plans if user just logged in
      if (window.location.pathname === "/meal-planner.html") {
        fetchAndDisplayMealPlans();
      }
    } else {
      // User is signed out
      console.log("User is logged out.");
      if (loginSignUpBtn) {
        loginSignUpBtn.textContent = "Sign Up / Login";
        loginSignUpBtn.href = "#"; // Or to your login page URL
        // Remove existing listener to prevent multiple logout attempts
        const newBtn = loginSignUpBtn.cloneNode(true);
        loginSignUpBtn.parentNode.replaceChild(newBtn, loginSignUpBtn);
        newBtn.addEventListener("click", (e) => {
          e.preventDefault();
          window.location.href = "/login"; // Redirect to your login page
        });
      }
      if (myAccountLink) {
        myAccountLink.style.display = "none"; // Hide "My Account"
      }
    }
  });
}); // End of DOMContentLoaded

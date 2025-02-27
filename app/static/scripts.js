document.addEventListener('DOMContentLoaded', function() {
    const calorieProgress = document.getElementById('calorieProgress');
    const bmrProgress = document.getElementById('bmrProgress');
    const form = document.getElementById("calorieForm");
    const calorieResult = document.getElementById('calorieResult');
    const resultDiv = document.getElementById('result');
    const bmrResult = document.getElementById('bmrResult');
    const themeToggleButton = document.getElementById('theme-toggle');
    const bodyElement = document.body;

    // Check if the user has a previously saved theme in localStorage
    function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;
    }
    // function to toggle between light and dark theme
    themeToggleButton.addEventListener('click', function(){
       if (localStorage.getItem('theme') === 'theme-dark'){
           setTheme('theme-light');
       } else {
           setTheme('theme-dark');
    }
    });

    // Immediately invoked function to set the theme on initial load
    (function () {
       if (localStorage.getItem('theme') === 'theme-dark') {
           themeToggleButton.checked = true;
           setTheme('theme-dark');
       } else {
           setTheme('theme-light');
       }
    })();

    function calculateBMR(weight, height, age, gender) {
        let bmr = (10 * weight) + (6.25 * height) - (5 * age);
        bmr = gender === 'male' ? bmr + 5 : bmr - 161;
        return Math.round(bmr * form.fitness_level.value);
    }

    function animateNumber(element, endValue, progressElement) {
        const duration = 1500;
        const start = 0;
        const range = endValue - start;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Update number
            element.textContent = Math.round(progress * range).toLocaleString();

            // Update circular progress
            const progressPercentage = (progress * 100).toFixed(1);
            progressElement.style.background = `conic-gradient(var(--color-accent) ${progressPercentage}%, var(--bs-dark) ${progressPercentage}%)`;

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }



    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        if (!form.checkValidity()) {
        alert("Please fill in all required fields correctly.");
        return;
    }

        const data = {
            'age': parseInt(form.age.value),  // Accessing form element by name
            'gender': form.gender.value,  // Accessing form element by name (assuming 'gender' input is a radio button)
            'height_cm': parseFloat(form.height.value),
            'weight_kg': parseFloat(form.weight.value),
            'duration_minutes': parseInt(form.duration.value),
            'activity_type': form.activity_type.value,
            'intensity': form.intensity.value
        };

        try {
            const response = await fetch("https://zeeshan3155-calorie-calculator.hf.space/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });
            const result = await response.json();
            const bmr = calculateBMR(data["weight_kg"], data["height_cm"], data["age"], data["gender"]);
            // Display result with animation
            resultDiv.classList.remove('d-none');
            setTimeout(() => {
                resultDiv.classList.add('show');

                animateNumber(calorieResult, Math.round(result["calories_burned"]), calorieProgress);
                animateNumber(bmrResult, bmr, bmrProgress);
            }, 10);
        } catch (error) {
            document.getElementById("result").innerText = "Error fetching data!";
        }
    });
});
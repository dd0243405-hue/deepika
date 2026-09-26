// =========================================================
// EduGenie Frontend Application
// =========================================================


// ---------------------------------------------------------
// API endpoint mapping
// ---------------------------------------------------------

const taskMap = {
    qa: "/qa",
    explain: "/explain",
    quiz: "/quiz",
    summarize: "/summarize",
    recommendations: "/learn/recommendations"
};


// ---------------------------------------------------------
// Get DOM elements
// ---------------------------------------------------------

const taskSelect = document.getElementById("task");
const inputText = document.getElementById("inputText");
const submitButton = document.getElementById("submitBtn");
const statusElement = document.getElementById("status");
const resultCard = document.getElementById("resultCard");
const resultElement = document.getElementById("result");


// ---------------------------------------------------------
// Escape HTML
// ---------------------------------------------------------

function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


// ---------------------------------------------------------
// Render normal text
// ---------------------------------------------------------

function renderText(text) {

    return escapeHtml(text)
        .replace(/\n/g, "<br>");
}


// ---------------------------------------------------------
// Render quiz
// ---------------------------------------------------------

function renderQuiz(quiz) {

    return quiz.map((question, index) => {

        const options = question.options
            .map((option) => {

                return `
                    <li>
                        ${escapeHtml(option)}
                    </li>
                `;

            })
            .join("");


        return `
            <article class="quiz-question">

                <h3>
                    ${index + 1}.
                    ${escapeHtml(question.question)}
                </h3>

                <ol type="A">
                    ${options}
                </ol>

                <details>

                    <summary>
                        Show answer
                    </summary>

                    <p>
                        <strong>
                            ${escapeHtml(
                                question.correct_answer
                            )}
                        </strong>
                    </p>

                    <p>
                        ${escapeHtml(
                            question.explanation
                        )}
                    </p>

                </details>

            </article>
        `;

    }).join("");
}


// ---------------------------------------------------------
// Display status
// ---------------------------------------------------------

function setStatus(message) {

    statusElement.textContent = message;
}


// ---------------------------------------------------------
// Run selected EduGenie task
// ---------------------------------------------------------

async function runTask() {

    const task = taskSelect.value;

    const text = inputText.value.trim();


    // -----------------------------------------------------
    // Validate input
    // -----------------------------------------------------

    if (!text) {

        setStatus(
            "Please enter a question, concept, topic, or text."
        );

        inputText.focus();

        return;
    }


    // -----------------------------------------------------
    // Disable button
    // -----------------------------------------------------

    submitButton.disabled = true;

    submitButton.textContent = "Thinking...";

    setStatus(
        "EduGenie is generating your answer..."
    );


    resultCard.classList.add("hidden");

    resultElement.innerHTML = "";


    try {

        // -------------------------------------------------
        // Send request to FastAPI
        // -------------------------------------------------

        const response = await fetch(
            taskMap[task],
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text
                })
            }
        );


        // -------------------------------------------------
        // Parse response
        // -------------------------------------------------

        const data = await response.json();


        // -------------------------------------------------
        // Handle API error
        // -------------------------------------------------

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "The server returned an error."
            );
        }


        // -------------------------------------------------
        // Quiz response
        // -------------------------------------------------

        if (data.quiz) {

            resultElement.innerHTML =
                renderQuiz(data.quiz);

        }

        // -------------------------------------------------
        // Normal text response
        // -------------------------------------------------

        else if (data.result) {

            resultElement.innerHTML = `
                <div class="answer">
                    ${renderText(data.result)}
                </div>
            `;

        }

        // -------------------------------------------------
        // Unexpected response
        // -------------------------------------------------

        else {

            throw new Error(
                "The server returned an unexpected response."
            );
        }


        // -------------------------------------------------
        // Show result
        // -------------------------------------------------

        resultCard.classList.remove("hidden");

        setStatus(
            "Completed successfully."
        );


        // Scroll to result
        resultCard.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }

    catch (error) {

        console.error(
            "EduGenie error:",
            error
        );


        setStatus(
            error.message ||
            "Something went wrong. Please try again."
        );

    }

    finally {

        submitButton.disabled = false;

        submitButton.textContent = "✨ Generate";

    }
}


// ---------------------------------------------------------
// Copy result
// ---------------------------------------------------------

async function copyResult() {

    const text =
        resultElement.innerText.trim();


    if (!text) {

        setStatus(
            "There is no result to copy."
        );

        return;
    }


    try {

        await navigator.clipboard.writeText(
            text
        );


        setStatus(
            "Result copied to clipboard."
        );

    }

    catch (error) {

        console.error(
            "Copy error:",
            error
        );


        setStatus(
            "Unable to copy the result."
        );
    }
}


// ---------------------------------------------------------
// Keyboard shortcut
//
// Ctrl + Enter = Generate
// ---------------------------------------------------------

inputText.addEventListener(
    "keydown",
    (event) => {

        if (
            event.ctrlKey &&
            event.key === "Enter"
        ) {

            event.preventDefault();

            runTask();
        }

    }
);


// ---------------------------------------------------------
// Allow Enter shortcut on Mac
// Cmd + Enter = Generate
// ---------------------------------------------------------

inputText.addEventListener(
    "keydown",
    (event) => {

        if (
            event.metaKey &&
            event.key === "Enter"
        ) {

            event.preventDefault();

            runTask();
        }

    }
);
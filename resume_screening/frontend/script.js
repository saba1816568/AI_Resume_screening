document.getElementById("resume-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    let files = document.getElementById("files").files;
    let jobDescription = document.getElementById("job-description").value;

    if (files.length === 0 || !jobDescription) {
        alert("Please upload resumes and enter a job description!");
        return;
    }

    let filePaths = [];
    for (let file of files) {
        filePaths.push(file.name);  // Store only file names
    }

    let requestData = {
        resumes: filePaths,  // Sending only file paths
        job_description: jobDescription
    };

    // let formData = new FormData();
    // for (let file of files) {
    //     formData.append("resumes", file);
    // }
    // formData.append("job_description", jobDescription);
    console.log('req',JSON.stringify(requestData))
    try {
        let response = await fetch("http://127.0.0.1:8000/rank_resumes/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"  // ✅ Ensure JSON format
            },
            body: JSON.stringify(requestData),
        });
        
        let result = await response.json();
        console.log(result)
        displayResults(result.ranked_resumes);
    } catch (error) {
        console.error("Error:", error);
    }
});

function displayResults(rankedResumes) {
    let resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = "";

    rankedResumes.forEach(([index, score]) => {
        let listItem = document.createElement("li");
        listItem.textContent = `Resume ${index + 1} - Score: ${score.toFixed(2)}`;
        resultsContainer.appendChild(listItem);
    });
}

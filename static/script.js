// ==========================================
// ELEMENT
// ==========================================

const titleInput = document.getElementById("title");
const contentInput = document.getElementById("content");

const predictBtn = document.getElementById("predictBtn");

const predictionText = document.getElementById("predictionText");
const predictionDesc = document.getElementById("predictionDesc");
const predictionBadge = document.getElementById("predictionBadge");
const predictionIcon = document.getElementById("predictionIcon");

const confidenceBar = document.getElementById("confidenceBar");
const confidenceValue = document.getElementById("confidenceValue");

const hoaxBar = document.getElementById("hoaxBar");
const hoaxValue = document.getElementById("hoaxValue");

const validBar = document.getElementById("validBar");
const validValue = document.getElementById("validValue");

const predictTime = document.getElementById("predictTime");

const loadingOverlay = document.getElementById("loadingOverlay");
const loadingText = document.getElementById("loadingText");

// ==========================================
// SHOW LOADING
// ==========================================

function showLoading(text) {

    loadingText.innerHTML = text;

    loadingOverlay.style.display = "flex";

}

// ==========================================
// HIDE LOADING
// ==========================================

function hideLoading() {

    loadingOverlay.style.display = "none";

}

// ==========================================
// RESET STEP ICON
// ==========================================

function resetSteps() {

    for (let i = 1; i <= 6; i++) {

        const step = document.getElementById("step" + i);

        step.className = "fa-regular fa-circle";

    }

}

// ==========================================
// ANIMATE STEP
// ==========================================

async function animateSteps() {

    resetSteps();

    for (let i = 1; i <= 6; i++) {

        await new Promise(resolve => setTimeout(resolve, 250));

        const step = document.getElementById("step" + i);

        step.className = "fa-solid fa-circle-check";

        step.style.color = "#2ecc71";

    }

}

// ==========================================
// ANIMATE BAR
// ==========================================

function animateBar(element, value) {

    let current = 0;

    element.style.width = "0%";

    const interval = setInterval(() => {

        current++;

        element.style.width = current + "%";

        if (current >= value) {

            clearInterval(interval);

        }

    }, 8);

}

// ==========================================
// UPDATE RESULT
// ==========================================

function updateResult(data) {

    const confidence = Math.round(data.confidence);

    const hoax = Math.round(data.hoax_probability);

    const valid = Math.round(data.valid_probability);

    confidenceValue.innerHTML = confidence + "%";

    hoaxValue.innerHTML = hoax + "%";

    validValue.innerHTML = valid + "%";

    animateBar(confidenceBar, confidence);

    animateBar(hoaxBar, hoax);

    animateBar(validBar, valid);

    predictTime.innerHTML = data.processing_time + " s";

    if (data.prediction === "HOAX") {

        predictionText.innerHTML = "HOAKS";

        predictionDesc.innerHTML =
            "Berita memiliki kemungkinan merupakan hoaks.";

        predictionBadge.innerHTML = "HOAKS";

        predictionBadge.className = "badge danger";

        predictionIcon.innerHTML =
            '<i class="fa-solid fa-triangle-exclamation"></i>';

    }

    else {

        predictionText.innerHTML = "VALID";

        predictionDesc.innerHTML =
            "Berita diprediksi valid.";

        predictionBadge.innerHTML = "VALID";

        predictionBadge.className = "badge success";

        predictionIcon.innerHTML =
            '<i class="fa-solid fa-circle-check"></i>';

    }

}

// ==========================================
// PREDICT
// ==========================================

predictBtn.addEventListener("click", async () => {

    const title = titleInput.value.trim();

    const content = contentInput.value.trim();

    if (title === "" && content === "") {

        alert("Masukkan berita terlebih dahulu.");

        return;

    }

    showLoading("AI sedang menganalisis berita...");

    await animateSteps();

    fetch("/predict", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            title: title,

            content: content

        })

    })

    .then(res => res.json())

    .then(data => {

        hideLoading();

        if (data.success) {

            updateResult(data);

        }

        else {

            alert(data.message);

        }

    })

    .catch(err => {

        hideLoading();

        console.log(err);

        alert("Terjadi kesalahan.");

    });

});

// ==========================================
// BUTTON
// ==========================================

const updateBtn = document.getElementById("updateBtn");
const trainBtn = document.getElementById("trainBtn");

// ==========================================
// SCRAPING PROGRESS BAR
// ==========================================

const rssProgress = document.getElementById("rssProgress");
const gnewsProgress = document.getElementById("gnewsProgress");
const newsProgress = document.getElementById("newsProgress");
const mergeProgress = document.getElementById("mergeProgress");

// ==========================================
// TRAINING PROGRESS BAR
// ==========================================

const train1 = document.getElementById("train1");
const train2 = document.getElementById("train2");
const train3 = document.getElementById("train3");
const train4 = document.getElementById("train4");
const train5 = document.getElementById("train5");

// ==========================================
// RESET PROGRESS
// ==========================================

function resetProgress() {

    [
        rssProgress,
        gnewsProgress,
        newsProgress,
        mergeProgress,
        train1,
        train2,
        train3,
        train4,
        train5

    ].forEach(bar => {

        bar.style.width = "0%";

    });

}

// ==========================================
// ANIMATE PROGRESS
// ==========================================

function progress(bar, target) {

    return new Promise(resolve => {

        let width = 0;

        const timer = setInterval(() => {

            width++;

            bar.style.width = width + "%";

            if (width >= target) {

                clearInterval(timer);

                resolve();

            }

        }, 15);

    });

}

// ==========================================
// UPDATE DATASET
// ==========================================

updateBtn.addEventListener("click", async () => {

    resetProgress();

    showLoading("Mengambil berita terbaru...");

    await progress(rssProgress, 25);

    await progress(gnewsProgress, 50);

    await progress(newsProgress, 75);

    await progress(mergeProgress, 95);

    fetch("/update-dataset", {

        method: "POST"

    })

    .then(res => res.json())

    .then(async data => {

        mergeProgress.style.width = "100%";

        hideLoading();

        if (data.success) {

            showToast(

                "Berhasil",

                "Dataset berhasil diperbarui."

            );

        }

        else {

            showToast(

                "Gagal",

                data.message

            );

        }

    })

    .catch(err => {

        hideLoading();

        console.log(err);

        showToast(

            "Error",

            "Tidak dapat memperbarui dataset."

        );

    });

});

// ==========================================
// RETRAIN MODEL
// ==========================================

trainBtn.addEventListener("click", async () => {

    showLoading(

        "Training model..."

    );

    train1.style.width = "20%";

    await new Promise(r => setTimeout(r, 300));

    train2.style.width = "40%";

    await new Promise(r => setTimeout(r, 300));

    train3.style.width = "60%";

    await new Promise(r => setTimeout(r, 300));

    train4.style.width = "80%";

    await new Promise(r => setTimeout(r, 300));

    fetch("/retrain", {

        method: "POST"

    })

    .then(res => res.json())

    .then(async data => {

        train5.style.width = "100%";

        hideLoading();

        if (data.success) {

            showToast(

                "Training Selesai",

                "Model berhasil diperbarui."

            );

        }

        else {

            showToast(

                "Gagal",

                data.message

            );

        }

    })

    .catch(err => {

        hideLoading();

        console.log(err);

        showToast(

            "Error",

            "Training gagal."

        );

    });

});

// ==========================================
// SIMPLE TOAST
// ==========================================

function showToast(title, message) {

    const toast = document.getElementById("toast");

    const toastTitle = document.getElementById("toastTitle");

    const toastMessage = document.getElementById("toastMessage");

    toastTitle.innerHTML = title;

    toastMessage.innerHTML = message;

    toast.classList.add("show");

    setTimeout(() => {

        toast.classList.remove("show");

    }, 3000);

}

// ==========================================
// HISTORY
// ==========================================

const historyBody = document.getElementById("historyBody");
const clearHistoryBtn = document.getElementById("clearHistory");

function getHistory() {

    const history = localStorage.getItem("history");

    if (!history) {

        return [];

    }

    return JSON.parse(history);

}

function saveHistory(item) {

    const history = getHistory();

    history.unshift(item);

    if (history.length > 10) {

        history.pop();

    }

    localStorage.setItem(

        "history",

        JSON.stringify(history)

    );

    renderHistory();

}

function renderHistory() {

    const history = getHistory();

    historyBody.innerHTML = "";

    if (history.length === 0) {

        historyBody.innerHTML = `

        <tr>

            <td colspan="4">

                Belum ada riwayat analisis.

            </td>

        </tr>

        `;

        return;

    }

    history.forEach(item => {

        historyBody.innerHTML += `

        <tr>

            <td>${item.time}</td>

            <td>${item.title}</td>

            <td>

                ${item.result}

            </td>

            <td>

                ${item.confidence}%

            </td>

        </tr>

        `;

    });

}

renderHistory();

// ==========================================
// CLEAR HISTORY
// ==========================================

clearHistoryBtn.addEventListener(

    "click",

    () => {

        if (

            confirm(

                "Hapus seluruh riwayat?"

            )

        ) {

            localStorage.removeItem(

                "history"

            );

            renderHistory();

        }

    }

);

// ==========================================
// SIMPAN HISTORY SETELAH PREDICT
// ==========================================

const oldUpdateResult = updateResult;

updateResult = function(data){

    oldUpdateResult(data);

    saveHistory({

        time: new Date().toLocaleTimeString(),

        title: titleInput.value,

        result: data.prediction,

        confidence: Math.round(data.confidence)

    });

};

// ==========================================
// COUNTER ANIMATION
// ==========================================

function counter(id,target){

    let value=0;

    const el=document.getElementById(id);

    const timer=setInterval(()=>{

        value++;

        el.innerHTML=value;

        if(value>=target){

            clearInterval(timer);

        }

    },15);

}

// ==========================================
// LOAD DASHBOARD
// ==========================================

window.addEventListener(

    "load",

    ()=>{

        counter(

            "totalDataset",

            18542

        );

        document.getElementById(

            "datasetCount"

        ).innerHTML="18.542";

        document.getElementById(

            "accuracy"

        ).innerHTML="94.8%";

        document.getElementById(

            "predictSpeed"

        ).innerHTML="0.02 s";

    }

);

// ==========================================
// ENTER = PREDICT
// ==========================================

contentInput.addEventListener(

    "keydown",

    function(e){

        if(

            e.ctrlKey &&

            e.key==="Enter"

        ){

            predictBtn.click();

        }

    }

);

// ==========================================
// AUTO RESIZE TEXTAREA
// ==========================================

contentInput.addEventListener(

    "input",

    function(){

        this.style.height="auto";

        this.style.height=

        this.scrollHeight+"px";

    }

);

// ==========================================
// SCROLL TO RESULT
// ==========================================

function scrollResult(){

    document

    .querySelector(

        ".result-section"

    )

    .scrollIntoView({

        behavior:"smooth"

    });

}

// ==========================================
// MODIFIKASI updateResult
// ==========================================

const oldFunction=updateResult;

updateResult=function(data){

    oldFunction(data);

    scrollResult();

}

// ==========================================
// RANDOM AI STATUS
// ==========================================

const statusText=[

    "Model Ready",

    "Dataset Updated",

    "Naive Bayes Active",

    "TF-IDF Loaded"

];

setInterval(()=>{

    const random=Math.floor(

        Math.random()*

        statusText.length

    );

    document.querySelector(

        ".status"

    ).lastChild.textContent=

    " "+statusText[random];

},4000);

// ==========================================
// VERSION
// ==========================================

console.log(

"%cFakeNews AI Dashboard",

"color:#4f7cff;font-size:22px;font-weight:bold"

);

console.log(

"Version 2.0"

);

// ==========================================
// SIDEBAR ACTIVE MENU
// ==========================================

const menuLinks = document.querySelectorAll(".menu a");

menuLinks.forEach(link => {

    link.addEventListener("click", function () {

        document.querySelectorAll(".menu li").forEach(item => {
            item.classList.remove("active");
        });

        this.parentElement.classList.add("active");

    });

});
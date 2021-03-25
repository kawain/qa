const qaform = document.getElementById("qaform")
const display1 = document.getElementById("display1")
const display2 = document.getElementById("display2")
const qbtn = document.getElementById("qbtn")
const mondai = document.getElementById("mondai")


function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1)); // 0 から i のランダムなインデックス
        [array[i], array[j]] = [array[j], array[i]]; // 要素を入れ替えます
    }
}

function makeList(n) {
    let arr = []
    for (let i = 0; i < n; i++) {
        arr.push(i)
    }
    return arr
}

function questionQuestions(arr, data) {
    let i = 0
    function func() {
        if (i >= arr.length) {
            return false
        }
        let index = arr[i]
        i++
        return [data[index], i]
    }
    return func;
}

function changeQuestion(func) {
    let obj = func()
    if (!obj) {
        display1.innerHTML = "問題は終了しました<br><br><br>"
        display2.innerHTML = ""
    } else {
        let html1 = `<p>No ${obj[1]}. ${obj[0].cat__name}の問題</p><pre><code>${obj[0].problem}</code></pre>`
        let html2 = `<p>解答：<b style="color:#fff;">${obj[0].answer}</b></p>`
        display1.innerHTML = html1
        display2.innerHTML = html2
    }
}

function shuffleData(data) {
    let count = data.length
    let arr = makeList(count)
    shuffle(arr)
    let qq = questionQuestions(arr, data)
    qbtn.addEventListener("click", () => {
        changeQuestion(qq)
    })
}

if (qaform) {
    const c = document.getElementsByName("c")
    qaform.addEventListener("submit", (e) => {
        e.preventDefault()

        mondai.style.display = "block"

        display1.innerHTML = ""
        display2.innerHTML = ""

        // ?c=2&c=8
        let params = "?"
        for (v of c) {
            if (v.checked) {
                params += `c=${v.value}&`
            }
        }
        fetch(`/qa/start/${params}`).then(response => {
            return response.json()
        }).then(jsonData => {
            shuffleData(jsonData)
        });
    })
}
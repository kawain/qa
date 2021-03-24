const qaform = document.getElementById("qaform")
const display1 = document.getElementById("display1")
const display2 = document.getElementById("display2")
const qbtn = document.getElementById("qbtn")


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
        if (i == arr.length) {
            return
        }
        let index = arr[i]
        i++
        return data[index]
    }
    return func;
}

function changeQuestion(func) {
    let obj = func()
    let html1 = `<pre><code>${obj.fields.problem}</code></pre>`
    let html2 = `<p>解答：<b style="color:#fff;">${obj.fields.answer}</b></p>`
    display1.innerHTML = html1
    display2.innerHTML = html2
}

function shuffleData(data) {
    const obj = JSON.parse(data.qa_json);
    let count = obj.length
    let arr = makeList(count)
    shuffle(arr)
    let qq = questionQuestions(arr, obj)
    qbtn.addEventListener("click", () => {
        changeQuestion(qq)
    })
}

if (qaform && display1 && display2 && qbtn) {
    const c = document.getElementsByName("c")
    qaform.addEventListener("submit", (e) => {
        e.preventDefault()

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
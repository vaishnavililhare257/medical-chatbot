async function sendMessage(){

let input = document.getElementById("userInput")
let message = input.value

if(message==="") return

let chatbox = document.getElementById("chatbox")

chatbox.innerHTML += `<div class="user">👤 ${message}</div>`

input.value=""

let response = await fetch("http://127.0.0.1:8000/chat",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({query:message})
})

let data = await response.json()

chatbox.innerHTML += `<div class="bot">🤖 ${data.answer}</div>`

chatbox.scrollTop = chatbox.scrollHeight
}
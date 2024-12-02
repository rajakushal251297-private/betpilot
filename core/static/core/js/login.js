

document.getElementById("loginbtnid").addEventListener("click", function(){
    const username=document.getElementById("usernameid").value;
    const password= document.getElementById("passwordid").value;
    if(username.trim() !="" && password.trim() !=""){
        let formdata;
        formdata= new FormData();
        formdata.append("username",username);
        formdata.append("password",password);
        console.log("logged in");
        fetch("/",
            {
            method: "POST",
            body: formdata
        }).then(response => response.json())
        .then(data => {
            if (data.status == "success"){
                window.location.href = "/home";
            }
            else{
                alert(data.status);
            }
        })
    }else{
        alert("Both username and password are required");
    }
})

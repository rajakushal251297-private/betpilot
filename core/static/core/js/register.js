

document.getElementById("loginbtnid").addEventListener("click", function(){
    const username=document.getElementById("usernameid").value;
    const password1= document.getElementById("passwordid1").value;
    const password2= document.getElementById("passwordid2").value;
    if(username.trim() !="" && password1.trim() !="" && password2.trim() !=""){
        let formdata;
        formdata= new FormData();
        formdata.append("username",username);
        formdata.append("password",password1);
        formdata.append("confirm_password",password2);
        console.log("logged in");
        fetch("/register/",
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

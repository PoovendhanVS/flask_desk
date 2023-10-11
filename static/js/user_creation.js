function go_to_login(name,pwd){
    $.ajax({    
        url: '/get_login',
        type: 'POST', 
        data: { 
            'name': name,
            'pwd': pwd 
        },
        success: function (data) {
            if (data == "Success"){
                alert('Your are successfully login.');
                window.location.href='/dashboard';
            }
            else{
                alert(data);
                // window.location.href='/';
            }
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}

function user_create(usertype, name, email, pwd) {
    $.ajax({    
        url: '/user_create',
        type: 'POST', 
        data: { 
            'usertype' : usertype,
            'name': name,
            'email': email,
            'pwd': pwd 
        },
        success: function (data) {
            if (data == "Success"){
                // alert('User is created successfully.');
                window.location.href='/user_creation';
            }
            else{
                alert(data);
                window.location.href='/signup';
            }
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}
function update_user(usertype, id, name, email, pwd) {
    $.ajax({    
        url: '/edit_user',
        type: 'POST', 
        data: { 
            'usertype' : usertype,
            'user_id' : id,
            'name': name,
            'email': email,
            'pwd': pwd 
        },
        success: function (data) {
            if(data == 'Success'){
            // alert('User details updated successfully.');
            window.location.href = '/user_creation';
            }else{
                alert(data);
            }
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}
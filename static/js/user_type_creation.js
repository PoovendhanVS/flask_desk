function create_user_type(user_type, status){
    $.ajax({    
        url: '/insert_user_type',
        type: 'POST', 
        data: { 
            'usertype' : user_type,
            'status': status,
        },
        success: function (data) {
            if(data == 'Success'){
                alert('Inserted')
            window.location.href = '/user_type_creation';
            }else{
                alert(data);
            }
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}

function update_user_type(user_type_id, user_type, status) {
    $.ajax({    
        url: '/edit_user_type',
        type: 'POST', 
        data: { 
            'id' : user_type_id,
            'name' : user_type,
            'status' : status,
        },
        success: function (data) {
            if(data == 'Success'){
            window.location.href = '/user_type_creation';
            }else{
                alert(data);
            }
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}
function company_create(com_name,com_address,bill_name,bill_address,mobile,phone,gst){
    $.ajax({  
        url: '/insert_company',
        type: 'POST', 
        data: { 
            'com_name' : com_name,
            'com_address' : com_address,
            'bill_name' : bill_name,
            'bill_address' : bill_address,
            'mobile' : mobile,
            'phone' : phone,
            'gst' : gst
        },
        success: function (data) {
            if(data == 'Success'){
                alert('Inserted')
            window.location.href = '/company_creation';
            }else{
                alert(data);
                window.location.href = '/create_company';
            }
        },
        error: function (error) {
            alert(error),
            console.error('Error:', error);
        }
    });
}
function update_company_details(com_id,com_name,com_address,bill_name,bill_address,mobile,phone,gst){
    $.ajax({  
        url: '/edit_company_details',
        type: 'POST', 
        data: { 
            'com_id' : com_id,
            'com_name' : com_name,
            'com_address' : com_address,
            'bill_name' : bill_name,
            'bill_address' : bill_address,
            'mobile' : mobile,
            'phone' : phone,
            'gst' : gst
        },
        success: function (data) {
            if(data == 'Success'){
                alert('Updated')
            window.location.href = '/company_creation';
            }else{
                alert(data);
                window.location.href = '/create_company';
            }
        },
        error: function (error) {
            alert(error),
            console.error('Error:', error);
        }
    });
}

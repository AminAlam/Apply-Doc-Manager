// Reply box popup JS
$(document).ready(function(){
    $(".reply-popup").click(function(){
      $(".reply-box").toggle();
    });
  });


  function onSubmit(token) {
    document.getElementById("demo-form").submit();
  }



window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove(); 
    });
}, 2000);

$(document).ready(function(){
    
    $("#livebox").on("input",function(e){
        $("#datalist").empty();
        $.ajax({
            method:"post",
            url:"/livesearch",
            data:{text:$("#livebox").val()},
            success:function(res){
                var data = "";
                $.each(res,function(index,value){
                    data += "<a class='search dropdown-item ' href=/"+value[3]+">";
                    data += value[0]+" | "+value[7]+" | "+value[1];
                    data += "</a>";
                });
                data += "</ul>";
                $("#datalist").html(data);
            }
        });
    });
});


$(document).ready(function(){
    
    $("#UniSearch").on("input",function(e){
        $("#UniSearch_datalist").empty();
        $.ajax({
            method:"post",
            url:"/DataSearch",
            data:{text:$("#UniSearch").val()},
            success:function(res){
                var data = "";
                $.each(res,function(index,value){
                    data += "<a class='search dropdown-item ' href=/"+value[0]+">";
                    data += value[1]+"</a>";
                });
                data += "</ul>";
                $("#UniSearch_datalist").html(data);
            }
        });
    });
});



$(document).ready(function(){
    $("#University").on("change",function(e){
        $("#Department").empty(); 
        $.ajax({
            method:"post",
            url:"/Department4Uni",
            data:{text:$("#University").val()},
            success:function(res){
                var data = "";
                $.each(res,function(index,value){
                     
                     data += "<option value="+value[0]+">"+value[0]+"</option>";
                    });
                $("#Department").html(data);
            }
        });
    });
});


$(document).ready(function(){
    $("#Department").on("click",function (e){
        const elem = document.querySelector("#Department")
        if (elem.childNodes.length==1){
        $("#Department").empty(); 
        $.ajax({
            method:"post",
            url:"/Department4Uni",
            data:{text:$("#University").val()},
            success:function(res){
                var data = "";
                $.each(res,function(index,value){
                     
                     data += "<option value="+value[0]+">"+value[0]+"</option>";
                    });
                $("#Department").html(data);
            }
        });
    }
    });
}, {once : true});




window.onload = function(){
	var popup = document.getElementById('datalist');
    var SearchBarMainBox = document.getElementById('SearchBarMainBox');
    document.onclick = function(e){
        if(e.target.id != 'livebox'){
            popup.style.display = 'none';
            SearchBarMainBox.style.boxShadow =  "none";
            // overlay.style.display = 'none';
        }
        if(e.target.id =='livebox' ){
            popup.style.display = 'block';
            SearchBarMainBox.style.boxShadow =  "0px 0px 15px 4px rgba(0, 0, 0, 0.3)";
            // overlay.style.display = 'none';
        }

    };
};



document.querySelector('.custom-file-inputName2').addEventListener('change', function(e) {
    var fileName = "";
    var nextSibling = e.target.nextElementSibling  ;
    var len = 0
    for (let i in document.getElementById("myInput2").files) {
        len = len + 1;
    }
    if (len>2){
        len = len - 2;
        fileName = len.toString();
        fileName = fileName.concat(" Files Selected");
        if (len==1){
            fileName = len.toString().concat(" File Selected"); 
        }
    }
    else {

        fileName = "Data File/Files";

    }
    nextSibling.innerText = fileName;
})




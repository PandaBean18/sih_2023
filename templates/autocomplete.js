let availableKeywords = ['HTML','CSS','EASY TUTORIALS'];

const resultBox = document.querySelector(".result-box");
const inputbox = document.getElementById("input-box");

inputbox.onkeyup = function(){
    let result = [];
    let input = inputbox.ariaValue;
    if(input.length){
      return  result=availableKeywords.filter((keyword.toLowerCase())=>{keyword.includes(input.toLowerCase());
        })
        console.log(result);
    } 
    display(result);

    if(result.length){resultBox.innerHTML = '';}
}

function display(result){
    const content = result.map((list)=>{
    return "<li onclick=selectInput(this)>"+list+"</li>";
    });

    resultBox.innerHTML = "<ul>"+content.join('')+"</ul>";
}

function selectInput(list){
    inputbox.value = list.innerhtml;
    resultsBox.innerHTML = '';
}


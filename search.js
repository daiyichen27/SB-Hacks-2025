let recipes = new Map();
let foodScore = new Array();
var data;
var input;
var index;

var requirejs = require(['https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js'], function (requirejs) {});

window.onload = function() {
    document.getElementById("submit").onclick = function fun() {
        onSubmit();
    }
};

async function getData(jsonData) {
    data = JSON.parse(jsonData);
}

async function onSubmit() {
    index = 0;
    input = document.getElementById("ingredients").value;
    input = input.replace(/[\s\n]/g, '');

    await $.ajax({
        type: "GET", 
        url: "/fridgecheck",
        // http://localhost:5000/fridgecheck
        // http://127.0.0.1:5000/fridgecheck
        data: {'ingredients': input},
        success: function(jsonData) {
            getData(jsonData.result);
        }
    });
    for (const recipe of data) {
        let perc = recipe.usedIngredientCount/(recipe.usedIngredientCount + recipe.missedIngredientCount);
        foodScore.push([recipe.title, perc]);
    }
    foodScore.sort(function(a, b) {
        return b[1] - a[1];
    });

    while (index < foodScore.length && index < 10) {
        let info = document.createElement("p");
        info.innerText = foodScore[index][0] + " " 
                        + (foodScore[index][1].toPrecision(3)*100) + "%"
                        + " of ingredients";
        document.body.appendChild(info);
        index++;
    }

    let showMoreButton = document.getElementById("showMore");
    showMoreButton.hidden = false;
}

function checkFoods() {
    var fridge = input.split(',');
    console.log(fridge);
    for (const key of recipes.keys()) {
        var required = recipes.get(key);
        var count = 0;
        for (const ingredient of required) {
            if (fridge.includes(ingredient)) {
                count += 1;
            }
        }
        foodScore.push([key, count*1.0/required.length]);
    }
}

function printMore() {
    if (index > 0) {
        var tar = index+10;
        while (index < foodScore.length && index < tar) {
            let info = document.createElement("p");
            info.innerText = foodScore[index][0] + " " + (foodScore[index][1].toPrecision(3)*100) + "%";
            document.body.appendChild(info);
            index++;
        }
    }
}

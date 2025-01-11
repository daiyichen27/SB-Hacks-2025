let recipes = new Map();
let foodScore = new Array();
var input;
var index;

var requirejs = require(['https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js'], function (requirejs) {});

window.onload = function() {
    document.getElementById("submit").onclick = function fun() {
        onSubmit();
    }
};

function getData() {
    var data;
    readTextFile("https://github.com/daiyichen27/SB-Hacks-2025/blob/main/test.json", function(text){
        data = JSON.parse(text);
    });
    console.log(data);
    for (const recipe of data) {
        const ingredients = [];
        for (const ingredient of recipe.ingredients) {
            ingredients.push(ingredient.name.split(' ').join('').toLowerCase());
        }
        recipes.set(recipe.title, ingredients);
    }
}

function onSubmit() {
    index = 0;
    input = document.getElementById("ingredients").textContent;
    input.replace(/\s/g, '');

    $.ajax({
        type: "POST",
        url: "https:/inputdata",
        data: { "input": input },
        dataType: "json"
    });
    console.log('input posted');
    $.ajax({
        url: "https://github.com/daiyichen27/SB-Hacks-2025/blob/main/recipe_api.py",
    });
    getData();
    checkFoods();
    foodScore.sort(function(a, b) {
        return a[1] - b[1];
    });

    while (index < 10) {
        let info = document.createElement("p");
        info.innerText = foodScore[index][0] + " " + (foodScore[index][1].toPrecision(3)*100) + "%";
        document.body.appendChild(info);
        index++;
    }

    let getMoreButton = document.getElementById("getMore");
    getMoreButton.hidden = false;
}

function checkFoods() {
    var fridge = input.split(',');
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

function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}
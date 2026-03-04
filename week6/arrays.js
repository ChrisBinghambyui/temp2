const steps = ['one', 'two', 'three'];
steps.forEach(showSteps);
function showSteps(item){
    console.log(item)
};
let myList = document.querySelector('#myList');
const stepsHtml = steps.map(listTemplate);
function listTemplate(item) {
    return `<li>${item}</li>`
};
myList.innerHTML = stepsHtml;
let grades = ['A', 'B', 'C'];
let points;
let gpaPoints = grades.map(convert);
function convert(grade) {
    switch (grade){
        case 'A':
            points = 4;
            break;
        case 'B':
            points = 3;
            break;
        case 'C':
            points = 2;
            break;
        case 'D':
            points = 1;
            break;
        case 'F':
            points = 0;
            break;
        default:
            alert('not a valid grade');
    }
    return points;
}
let totalPoints = gpaPoints.reduce(getTotal);
function getTotal(total, item){
    return total + item
};
console.log(totalPoints);
let gpaAverage = totalPoints/gpaPoints.length;
console.log(gpaAverage);
const words = ['watermelon', 'peach', 'apple', 'tomato', 'grape'];
const shortWords = words.filter(function(word){
    return word.length <6;
})
console.log(shortWords);
const myArray = [12, 34, 21, 54];
const luckyNumber = 21;
let luckyIndex = myArray.indexOf(luckyNumber);
console.log(luckyIndex);
let container = document.querySelector('#studentContainer');
const students = [
    {last: 'Andrus', first: 'Aaron'},
    {last: 'Masa', first:'Manny'},
    {last: 'Tanda', first: 'Tamanda'}
];
students.forEach(function(item){
    let name = document.createElement('div');
    name.className = 'format';
    let html = `
        <span>${item.first}</span>
        <span>${item.last}</span>
        <hr>`;
    
    name.innerHTML = html
    container.appendChild(name);

})
const aCourse = {
    code: 'CSE121b',
    name: 'Javascript Language',
    logo: 'images/js-logo.webp',
    sections: [
    { sectionNum: 1, roomNum: 'STC 353', enrolled: 26, days: 'TTh', instructor: 'Bro T'},
    { sectionNum: 2, roomNum: 'STC 347', enrolled: 28, days: 'TTh', instructor: 'Sis A'}
    ],
    enrollStudent: function (sectionNum) {
        // find the right section...Array.findIndex will work here
        const sectionIndex = this.sections.findIndex(
          (section) => section.sectionNum == sectionNum
        );
        if (sectionIndex >= 0) {
          this.sections[sectionIndex].enrolled++;
          renderSections(this.sections);
        }
      }
  };

console.log(aCourse.code);
console.log(aCourse.name);

document.querySelector('#courseName').textContent = aCourse.name;
document.querySelector('#courseCode').textContent = aCourse.code;

document.querySelector('img').setAttribute('src', aCourse.logo);
document.querySelector('img').setAttribute('alt', aCourse.name);
document.querySelector('img').style.width='100px';

console.log(aCourse.sections[1].roomNum);

function sectionTemplate(section) {
    return `<tr>
      <td>${section.sectionNum}</td>
      <td>${section.roomNum}</td>
      <td>${section.enrolled}</td>
      <td>${section.days}</td>
      <td>${section.instructor}</td></tr>`
}

function renderSections(sections) {
const html = sections.map(sectionTemplate);
document.querySelector("#sections").innerHTML = html.join("");
}

renderSections(aCourse.sections);

document.querySelector("#enrollStudent").addEventListener("click", function () {
    const sectionNum = document.querySelector("#sectionNumber").value;
    aCourse.enrollStudent(sectionNum);
});

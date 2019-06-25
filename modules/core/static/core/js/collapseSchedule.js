/*
**  Спойлер для учебного плана на странице курса
*/

export default function collapseSchedule() {
  try {
      let collapseButton = document.querySelector('.course-schedule__title'),
          collapseContainer = document.querySelector('.schedule-list');

      collapseButton.addEventListener('click', function() {
        console.log('MODULE_COLLAPSE');
        collapseButton.classList.toggle('course-schedule__title_active');
        collapseContainer.classList.toggle('schedule-list_active');
      });
  } catch(e) {
      // console.error(e);
  }
}

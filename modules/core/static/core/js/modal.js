/*
**  Открытие/закрытие модального окна
*/
import { formElements } from './formSendMail';

export default function modal() {
  try {
      let modal = document.querySelector('.modal'),
          btnModalClose = document.getElementById('btnModalClose'),
          btnModalOpen = document.querySelectorAll('.button_modal_open');

      /*
      **  Открытие модального окна
      */
      for (let i = 0; i < btnModalOpen.length; i++) {
          btnModalOpen[i].addEventListener('click', function (e) {
              try {
                  e.preventDefault();
                  document.getElementById('phoneNumber').value = '';
                  modal.classList.add('modal_open');

                  formElements.modalDialog.classList.remove('modal__dialog_error');
                  formElements.modalDialogContent.innerHTML = 'Пожалуйста, введите номер, на который Вам перезвонить';
                  formElements.modalDialogTitle.innerHTML = 'Обратный звонок';
                  formElements.modalDialogForm.style.display = 'block';
              } catch (e) {
                  // console.error(e);
              }
          });
      }

      /*
      **  Закрытие модального окна по клику на кнопку и вне самого окна
      */
      btnModalClose.addEventListener('click', function () {
          modalClose();
      });

      document.addEventListener('click', function (e) {
          let _element = e.target;
          /*
          **  elem.classList.contains в нашем случае сопоставляет
          **  `modal` вот такому классу `modal modal_open`, т.е
          **  ищется полное совпадение, а нам нужно частичное
          */
          let _elementFirstClass = _element.className.split(' ');
          if (e.target.classList.contains('button_modal_open') || !modal.classList.contains(_elementFirstClass[0])) {
              return;
          } else {
              modalClose();
          }
      });

      function modalClose() {
          modal.classList.remove('modal_open');
          document.getElementById('btnSend').setAttribute('disabled', 'disabled');
          document.querySelector('.captcha p').style.display = 'none';
      }
  } catch(e) {
      // console.error(e);
  }
}

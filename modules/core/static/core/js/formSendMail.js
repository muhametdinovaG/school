/*
**  Форма отправки на почту
*/

let formElements;

function formSendMail () {
  try {
      let form = {};
      const FORM_URL = document.getElementById('formFeedback').dataset.feedback;
      let btnSend = document.getElementById('btnSend'),
          phoneNumber = document.getElementById('phoneNumber');
      /*
      **  Позволяем вводить только цифры
      */
      phoneNumber.addEventListener('keyup', function (e) {
          let _value = e.target.value;
          e.target.value = _value.replace(/[^0-9]/g, '');

          if (_value.length === 11) {
              btnSend.removeAttribute('disabled');
          } else {
              btnSend.setAttribute('disabled', 'disabled');
          }
      })

      /*
      **  Непосредственно отправка
      */
      form.modalDialog = document.querySelector('.modal__dialog');
      form.modalDialogTitle = document.querySelector('.dialog-content__title');
      form.modalDialogContent = document.querySelector('.dialog-content__body');
      form.modalDialogForm = document.querySelector('.modal__dialog .form');

      btnSend.addEventListener('click', function () {
          let _xhr = new XMLHttpRequest();
          _xhr.open('POST', FORM_URL, true);
          var data = new FormData(document.getElementById('formFeedback'));
          _xhr.send(data);

          _xhr.onreadystatechange = function () {
              /*
              ** ждём пока запрос будет завершен
               */
              if (_xhr.readyState !== 4) return;

              /*
              ** обрабатываем ответ от сервера
               */
              var _response = JSON.parse(_xhr.response);

              /*
              ** если не ввели или ввели неверно капчу
               */
              if (_response.error) {
                  document.querySelector('.captcha p').style.display = 'block';
              }

              /*
              ** если получили иную ошибку
               */
              if (_xhr.status !== 200) {
                  form.modalDialog.classList.add('modal__dialog_error');
                  form.modalDialogTitle.innerHTML = 'Ошибка';
                  form.modalDialogContent.innerHTML = 'Пожалуйста, повторите отправку формы.';
                  console.error(_xhr.statusText);
              } else {
                  form.modalDialog.classList.remove('modal__dialog_error');
                  form.modalDialogTitle.innerHTML = 'Спасибо!';
                  form.modalDialogContent.innerHTML = 'Мы перезвоним Вам в течении дня.';
                  form.modalDialogForm.style.display = 'none';
                  document.getElementById('phoneNumber').value = '';
              }
              /*
              ** всегда обновляем капчу
               */
              document.getElementById('id_captcha_1').value = '';
              document.getElementById('id_captcha_0').value = _response.cptch_key;
              document.querySelector('img.captcha').setAttribute('src', _response.cptch_image);
          }
      });

      formElements = form;
  } catch(e) {
      // console.error(e);
  }
}

export { formElements, formSendMail };
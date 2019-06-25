/*
**  Слайдер на странице `Галерея`
*/

export default function slider () {
  try {
      let slideIndex = 1,
          slide = document.getElementsByClassName('slider__item'),
          toNextSlide = document.getElementById('toNextSlide'),
          toPrevSlide = document.getElementById('toPrevSlide'),
          dots = document.getElementsByClassName('slider-dots__item'),
          touchStart = undefined, touchEnd = undefined;
      showSlides(slideIndex);

      toPrevSlide.addEventListener('click', function() {
        showSlides(slideIndex += -1);
      });

      toNextSlide.addEventListener('click', function() {
        showSlides(slideIndex += 1);
      });

      /*
      **  Swipe на touch-устройствах
      */
      for(let i = 0; i < slide.length; i++) {
        slide[i].addEventListener('touchstart', function(e) {
          touchStart = e.touches[0].clientX;
        });

        slide[i].addEventListener('touchend', function(e) {
          touchEnd = e.changedTouches[0].clientX;
          /*
          **  Swipe влево
          **
          **  Если swipe был непродолжительный или если его вовсе не было,
          **  то ничего не делаем
          **
          **  Чтобы увеличить/уменьшить продолжительность swipe для перехода
          **  к следующему слайду используется @let _step
          */
          let _step = 70;
          if(touchStart > touchEnd + _step){
            showSlides(slideIndex += 1);
          }
          /*
          **  Swipe вправо
          */
          else if(touchStart < touchEnd - _step){
            showSlides(slideIndex += -1);
          } else {
            return;
          }
        });
      }


      for(let i = 0; i < dots.length; i++) {
        dots[i].addEventListener('click', function() {
          showSlides(slideIndex = i + 1);
        });
      }

      function showSlides(n) {
        let _slides = document.getElementsByClassName('slider__item');
        if (n > _slides.length) {
          slideIndex = 1
        }
        if (n < 1) {
          slideIndex = _slides.length
        }

        for (let i = 0; i < _slides.length; i++) {
            _slides[i].style.display = 'none';
        }

        for (let i = 0; i < dots.length; i++) {
            dots[i].classList.remove('active');
        }
        _slides[slideIndex-1].style.display = 'block';
        dots[slideIndex - 1].classList.add('active');
      }
  } catch(e) {
      // console.error(e);
  }
}

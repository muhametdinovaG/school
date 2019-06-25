import collapseSchedule from './collapseSchedule';
import modal from './modal';
import { formSendMail } from './formSendMail';
import slider from './slider';
import '../sass/style.scss';

window.addEventListener('load', function() {
    collapseSchedule();
    slider();
    formSendMail();
    modal();
});
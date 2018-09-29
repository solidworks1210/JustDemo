/**
 * Created by sdn on 2017/3/20.
 */

function getFileName(filename){
    // 获取文件名字
    var inde = filename.lastIndexOf('.');
    if (inde == 0 || inde == filename.length){
                return filename
    }else{
        return filename.substring(0, inde)
    }
}

function getFileSuffix(filename){
    // 获取文件后缀
    var inde = filename.lastIndexOf('.');
    if (inde == 0 || inde == filename.length){
                return ''
    }else{
        return filename.substring(inde+1)
    }
}


// ******************************* cookie 操作 ******************
function getCookie(name) {
        var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return c ? c[1] : undefined;
    }
function delCookie(name) {
        var exp = new Date();
        exp.setTime(exp.getTime() - 1);
        var cval = getCookie(name);
        if (cval != null)
            document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
    }
function setCookie(name, value) {
        var Days = 30;
        var exp = new Date();
        exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
        document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
    }


//******************************** 时间操作 **********************
function time_id() {
    // 生成当前毫秒时间
    var myDate = new Date();
    var t_id = myDate.getMilliseconds();
    return t_id.toString()
}


// ****************************** 输入验证 ***********************
// 验证用户输入的各种方法

function verify_name(name_input){
    if(name_input.trim() !== ''){
        return true
    }else{
        return false
    }
}

function verify_ps(ps_input){
    if((ps_input.trim()).length >= 5){
        return true
    }else{
        return false
    }
}
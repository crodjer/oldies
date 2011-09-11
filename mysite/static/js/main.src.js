function toggleVisibility(id1, id2) 
{
  var e = document.getElementById(id1);
  var button = document.getElementById(id2);
  if(e.style.display == 'block')
  {
    e.style.display = 'none';
    //button.style.right = '0';
  }
  else
  {
    e.style.display = 'block';
    //button.style.right = '200px';
  }
}
function setCookie(c_name,value,expirehours)
{
  var exdate=new Date();
  exdate.setTime(exdate.getTime() + (expirehours * 3600 * 1000));
  document.cookie = c_name+ "=" +escape(value)+
  ((expirehours==null) ? "" : ";expires="+exdate.toUTCString())+";path=/";
}
function getCookie(c_name)
{
if (document.cookie.length>0)
  {
  c_start=document.cookie.indexOf(c_name + "=");
  if (c_start!=-1)
  {
  c_start=c_start + c_name.length+1;
  c_end=document.cookie.indexOf(";",c_start);
  if (c_end==-1) c_end=document.cookie.length;
  return unescape(document.cookie.substring(c_start,c_end));
  }
  }
return null;
}

function changeTheme(color){
  document.body.style.background='rgba('+ color +',0.8)';  
  setCookie("theme",color,144);   
}

function deleteElement(e){
  e.style.display = "none";
}

//There's my new js
window.onload = function () {
	document.getElementById("submit-btn").disabled = true;
	document.getElementById("id_file").onchange = function () {
		var ih = document.getElementById("tem-error");
		if ( ih ) {
			ih.innerHTML = "";
		};
		document.getElementById("ejs").style.display = "none";
		document.getElementById("submit-btn").disabled = true;
		document.getElementById("txt").innerHTML = this.value;
		if ( this.files[0].size > 500000 ) {
			document.getElementById("span-ejs").innerHTML = 'Error: Too big for a subtitle file';
			document.getElementById("ejs").style.display = 'block';
		};
		if ( this.files[0].size <= 500000 ) {
			document.getElementById("submit-btn").disabled = false;
		};
	};
};

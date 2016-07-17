var QUEUE =	MathJax.Callback.Queue();
var converter = Markdown.getSanitizingConverter();

function LivePreview(entryId, previewId, manualId, maxLength = 1000){
	this.entryId = entryId;
	this.previewId = previewId;
	this.flag = false;
	this.index = 0;
	this.interval = 100;

	this.entry = document.getElementById(entryId);
	this.base = document.getElementById(previewId);
	this.manual = document.getElementById(manualId);

	this.entry.live = this;
	this.manual.live = this;
	this.manual.disabled = true;

	this.preview = document.createElement("div");
	this.buffer = document.createElement("div");
	this.preview.id = "p_"+this.previewId;
	this.buffer.id = "b_"+this.previewId;

	this.base.appendChild(this.preview);
	this.base.appendChild(this.buffer);


	//this.preview.style.position = "absolute";
	//this.buffer.style.position = "absolute";
	this.preview.style.visibility = "block";
	this.buffer.style.visibility = "none";
	this.encoded = "";

	this.encodeMathJax = function(mathJax){
		// escape characters
		var encoded = mathJax.replace(/\\|`|\*|_|{|}|\[|\]|\(|\)|#|\+|\-|!|\./g, 
			function(c){
				return '\\'+c;
			}).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
		return encoded;
	}

	this.encodeHelper = function(entry){
		var init = 0;
		var isDouble = false;
		while (init < entry.length){
			if (entry[init] == '$'){
				if (init + 1 == entry.length){return entry;}
				else if (entry[init + 1] == '$'){
					if (init + 2 == entry.length){return entry;}
					isDouble = true;
					init += 2;
					break;
				}else{
					init += 1;
					break;
				}
			}
			init += 1;
		}
		if (init == entry.length){return entry;}

		var final = init;
		
		while (final < entry.length){
			if (entry[final] == '$'){
				if (final + 1 == entry.length){
					if (isDouble){return entry;}
					else {break;}
				}else{
					if (isDouble){
						if (entry[final + 1] == '$'){break;}
						else {return entry;}
					}else{
						if (entry[final + 1] != '$'){break;}
						else {return entry;}
					}
				}
			}
			final += 1;
		}
		
		if (final == entry.length){return entry;}

		var encodedPortion = this.encodeMathJax(entry.substring(init, final));
		var newInit = final + 1;
		var initString = '$';
		if (isDouble){newInit = final + 2; initString = '$$';}
		return entry.substring(0, init) + encodedPortion + initString + this.encodeHelper(entry.substring(newInit, entry.length));
	}

	this.encodeAllMathJax = function(){
		// encode all substrings of the form $...$ and $$...$$ in this.entry.value and save in this.encoded
		this.encoded = this.encodeHelper(this.entry.value);
	}


	this.updateBufferText = function(){
		this.flag = true;
		this.encodeAllMathJax();
		this.buffer.innerHTML = converter.makeHtml(this.encoded);
	};

	this.revealBuffer_HidePreview_Swap = function() {
		this.buffer.style.display = "block";
		this.preview.style.display = "none";
		var bufferTmp = this.buffer; var previewTmp = this.preview;
		this.buffer = previewTmp; this.preview = bufferTmp;
		this.flag = false;
	};

	this.raiseFlag = function() {
		this.flag = true;
	};

	this.lowerFlag = function() {
		this.flag = false;
	};

	this.avoidGlitch = function() {
		this.index -= 1;
		if (this.index == 0){
			if (this.flag){
				this.prerender();
			}else{
				this.render();
			}
		}
	};

	this.prerender = function(pass = false){
		if (this.entry.value.length < maxLength){
			this.manual.disabled = true;
		}else{
			this.manual.disabled = false;
		}
		if (this.entry.value.length < maxLength || pass){
			this.index += 1;
			setTimeout(function(live){live.avoidGlitch();}, this.interval, this);
		}
	};

	this.render = function() {
		this.updateBufferText();
		QUEUE.Push(["Typeset", MathJax.Hub, this.buffer]);
		QUEUE.Push([function(live){live.revealBuffer_HidePreview_Swap();}, this]);
		//alert(this.buffer.innerHTML + this.preview.innerHTML);
	};

	this.entry.addEventListener("keyup", function(){this.live.prerender();});
	this.manual.addEventListener("click", function(){this.live.prerender(true);});
}

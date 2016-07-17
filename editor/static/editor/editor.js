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

	this.preview.style.position = "static";
	this.buffer.style.position = "static";
	this.preview.style.display = "block";
	this.buffer.style.display = "none";

	this.updateBufferText = function(){
		this.flag = true;
		this.buffer.innerHTML = converter.makeHtml(this.entry.value);
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
	};

	this.entry.addEventListener("keyup", function(){this.live.prerender();});
	this.manual.addEventListener("click", function(){this.live.prerender(true);});
}

var dragging;
var changed = false;

//document.captureEvents(Event.MOUSEMOVE);

var doSimplePostXMLHttpRequest = function (url/*, ...*/) {
        var self = MochiKit.Async;
        var req = self.getXMLHttpRequest();
        if (arguments.length > 1) {
                var m = MochiKit.Base;
                var qs = m.queryString.apply(null, m.extend(null, arguments, 1));
        }
        req.open("POST", url, true);
        //taken from prototype, pretty much verbatim
            var requestHeaders =
                        ['X-Requested-With', 'XMLHttpRequest',
                         'X-MochiKit-Version', MochiKit.Async.VERSION,
                         'Accept', 'text/javascript, text/html, application/xml, text/xml, */*',
                         'Content-type', 'application/x-www-form-urlencoded'];
                /* Force "Connection: close" for Mozilla browsers to work around
                 * a bug where XMLHttpReqeuest sends an incorrect Content-length
                 * header. See Mozilla Bugzilla #246651.
                 */
                if (req.overrideMimeType) {
                        requestHeaders.push('Connection', 'close');
                }
                for (var i = 0; i < requestHeaders.length; i += 2) {
                    req.setRequestHeader(requestHeaders[i],
requestHeaders[i+1]);
                }

                return self.sendXMLHttpRequest(req, qs);

};



function doDown(e) {
  if (e.target.name) {
    if (e.target.name == "title") return true;
    if (e.target.name.substr(0,4) == "tags") return true;
  }
    document.onmousemove = doDrag;
    target = findDraggableParent(e.target);
    if (target == null) return;
    dragging = target;
    addElementClass(dragging,"dragging");
    return false;
}

function findDraggableParent(el) {
    if (el == null) return null;
    else if (hasElementClass(el,"draggable")) return el;
    else return findDraggableParent(el.parentNode);
}

function doDrag(e) {
    if (!dragging) return;
    target = findDraggableParent(e.target);
    if (target == null) return;
    if (target.id != dragging.id) {
        swapElements(target, dragging);
	changed = true;
    }
    return false;
}

function swapElements(child1, child2) {
    var parent = child1.parentNode;
    var children = parent.childNodes;
    var items = new Array();
    for (var i = 0; i < children.length; i++) {
        items[i] = children.item(i);
        if (children.item(i).id) {
            if (children.item(i).id == child1.id) items[i] = child2;
            if (children.item(i).id == child2.id) items[i] = child1;
        }
    }
    for (var i = 0; i < children.length; i++) {
        parent.removeChild(children.item(i));
    }
    for (var i = 0; i < items.length; i++) {
        parent.appendChild(items[i]);

    }
}

function doUp(e) {
    if (!dragging) return;
    removeElementClass(dragging,"dragging");
    addElementClass(dragging,"draggable");
    if (changed) {
        saveOrder();
    }

    dragging = null;
    document.onmousemove = null;
    changed = false;
    return false;
}

function debug(message) {
    t = document.createTextNode(message);
    $("debug").appendChild(t);
}

function saveOrder() {
    var ul = $("drag-container");
    var children = getElementsByTagAndClassName("div","draggable",ul);
    var idx = 1;
    var url = "?";
  var args = {};

    for (var i = 0; i < children.length; i++) {
      el = children[i];
        if (el.id) {
            if (el.id.indexOf("image") == 0) {
              id = el.id.split("-")[1];
              args["image-" + id] = idx;
              idx++;
            }
        }
    }
  doSimplePostXMLHttpRequest(url,args);
}

function stopprop(e) {
  e.stop();
  }

document.onmousedown=doDown;
document.onmouseup=doUp;


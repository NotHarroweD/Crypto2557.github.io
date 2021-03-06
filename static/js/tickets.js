(function(yourcode) {

  yourcode(window.jQuery, window.indexedDB, window, document);

}(function($, indexedDB, window, document) {

  $(function() {
    $(".requirement").each(function() {
      $this = $(this);
      idb.open('endless-farming-db').then(function(db) {
        var tx = db.transaction('units', 'readwrite');
        var store = tx.objectStore('units');
        return store.get(this.data("unit").replaceAll(" ", "_"));
      }.bind($this)).then(function(val) {
        var $progressbar = $(this.children().children()[0]);
        var requirement = $progressbar.attr('aria-valuemax');

        var value = 0;
        var val_text = 0;
        if (val != undefined) {
          value = 100 * ((val.nsr + val.sr) / parseFloat(requirement));
          val_text = val.nsr + val.sr;
        }
        $progressbar.attr('aria-valuenow', value);
        $progressbar.css("width", value + "%");
        if (value >= 100) {
          $progressbar.addClass("progress-bar-green");
        } else {
          $progressbar.addClass("progress-bar-red");
        }
        this.children().children()[0].innerText = (val_text) + "/" + requirement;
      }.bind($this));
    });
  });
}));
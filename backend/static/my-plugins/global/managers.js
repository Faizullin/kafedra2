class UrlFormatterManager {
    formatUrlById(url, record, args = {}, replace_str = "<int:pk>", record_field_name = "id") {
        let new_url = url.replace(replace_str, record[record_field_name]);
        if (Object.keys(args).length > 0) {
            new_url = new_url + "?";
            Object.keys(args).forEach(function (key) {
                new_url = new_url + "&" + key + "=" + args[key];
            });
        }
        return new_url;
    }
}


if (!window.managers) {
    window.managers = {
        checkManager(name) {
            if (window.managers[name]) {
                throw new Error(`Manager ${name} already exists`);
            }
        }
    };
    window.managers.checkManager('urlFormatter');
    window.managers.urlFormatter = new UrlFormatterManager();
} else {
    console.error('managers already defined');
}
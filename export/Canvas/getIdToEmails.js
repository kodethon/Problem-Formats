function getIdToEmails(config) {
    if(!config) config = {};
    if(!config.page) config.page = 1;
    if(!config.s) config.s = '';
    var course_id = location.pathname.split('/')[2];
    var url = 'https://' + location.hostname + '/api/v1/courses/' + course_id + '/users?enrollment_type[]=student&include[]=email&per_page=100&page=' + config.page;
    $.get(url, function(res) {
            console.log(url)
            for(var r in res) { 
                config.s += res[r].id + ',' + res[r].email + "\n"; 
            }
            if(res.length == 0) {
                if(config.callback) 
                    config.callback(config.s);
                else
                    (function() {
                        IdToEmails = config.s;
                        console.log('Run command: copy(IdToEmails)')
                    })()
            } else {
                getCanvasEmail({
                    page: config.page + 1,
                    callback: config.callback,
                    s : config.s
                });
            }
    });

}

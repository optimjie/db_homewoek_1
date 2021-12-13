class Show {
    constructor(root) {
        this.root = root;
        this.$show = $(`
<div>测试</div>
<div>
    <form action="/" method="post" enctype="multipart/form-data">
        <div><input type="file" multiple="multiple" accept="text/xml, application/xml" name="image"></div>
        <div><input type="submit" value="上传"></div>
    </form>
</div>
        `);
        this.root.$db_homework.append(this.$show);
    }
}

export class DbHomework {
    constructor(id) {
        this.id = id;
        console.log(id);
        this.$db_homework = $('#' + id);  // 获取了db_homework_12345678这个div
        this.menu = new Show(this);     
    }

    start() {

    }
}
<template>
    <div>
        <el-row>
            <el-col :span="16">
                <el-form :inline="true" :model="task_query">
                    <el-form-item>
                        <el-input v-model="task_query.name" clearable placeholder="任务名称"></el-input>
                    </el-form-item>
                    <el-form-item style="width:12%">
                    <el-select v-model="task_query.task_status" @change="task_search_by_status()" clearable placeholder="运行状态">
                        <el-option v-for="item in task_query.status_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                    </el-select>
                    </el-form-item>
                    <el-form-item style="width:12%">
                        <el-button type="primary" icon="el-icon-search" @click="task_search()">查询</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
            <el-col :span="8"  style="text-align: right">
                <el-button  icon="el-icon-refresh" @click="task_refresh()">刷新</el-button>
                <el-button v-if="has_permission('exploit_plugin_add')" type="primary" icon="el-icon-plus" @click="handle_task_add">新建任务</el-button>
            </el-col>
        </el-row>
        <el-row></el-row>
        <el-table :data="task_query.tasks.data" highlight-current-row :row-key="get_row_keys" v-loading="task_query.table_loading" style="width: 100%; margin-top: 20px">
            <el-table-column prop="name" label="任务名称"></el-table-column>
            <el-table-column prop="status" label="运行状态">
                <template slot-scope="scope">
                    <div v-if="scope.row.status==0">
                        未开始
                    </div>
                    <div v-if="scope.row.status==1">
                        执行中
                    </div>
                    <div v-if="scope.row.status==2">
                        已完成
                    </div>
                </template>
            </el-table-column>
            <el-table-column prop="create_time" label="创建时间"></el-table-column>
            <el-table-column prop="update_time" label="更新时间"></el-table-column>
            <el-table-column prop="start_time" label="执行时间"></el-table-column>
            <el-table-column prop="finish_time" label="结束时间"></el-table-column>
            <el-table-column prop="author" label="创建者"></el-table-column>
            <el-table-column label="操作" align="center" width="360px" v-if="has_permission('assets_host_edit|assets_host_del|assets_host_valid')">
                <template slot-scope="scope">
                    <el-button v-if="has_permission('assets_host_edit') && scope.row.status==0" size="small" icon="el-icon-video-play" @click="task_start(scope.row)">启动</el-button>
                    <el-button v-if="has_permission('assets_host_edit') && scope.row.status==1" size="small" icon="el-icon-circle-close" @click="task_stop(scope.row)">终止</el-button>
                    <el-button v-if="has_permission('assets_host_edit') && scope.row.status!=0" size="small" icon="el-icon-monitor" @click="task_detail_query(scope.row)">任务详情</el-button>
                    <el-button v-if="has_permission('assets_host_edit') && scope.row.status==0" size="small" icon="el-icon-edit" @click="task_edit(scope.row)">编辑</el-button>
                    <el-button v-if="has_permission('assets_host_edit') && (scope.row.status==-1 || scope.row.status==2)" size="small" icon="el-icon-edit" @click="task_start(scope.row)">重新运行</el-button>
                    <el-button v-if="has_permission('assets_host_del') && scope.row.status!=1" size="small" icon="el-icon-delete" type="danger" @click="task_delete(scope.row)"
                               :loading="task_query.btn_del_loading">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <div class="pagination-bar" v-if="task_query.tasks.total > 10">
            <el-pagination
                    @current-change="handle_task_current_change"
                    :current-page="task_query.current_task_page"  layout="total, prev, pager, next"
                    :total=" task_query.tasks.total">
            </el-pagination>
        </div>
        <el-dialog title="任务详情" :visible.sync="dialog_task_detail_visible" width="70%" :close-on-click-modal="false">
            <el-tabs v-model="task_detail.activeName">
                <el-tab-pane label="" name="first">
                    <el-row>
                        <el-col :span="16">
                            <el-form :inline="true" :model="task_detail">
                                <el-form-item>
                                    <el-input v-model="task_detail.attack_queue_target" clearable placeholder="目标IP/域名"></el-input>
                                </el-form-item>
                                <el-form-item style="width:18%">
                                <el-select v-model="task_detail.attack_queue_status" @change="attack_queue_query()" clearable placeholder="利用结果">
                                    <el-option v-for="item in task_detail.attack_queue_status_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                                </el-select>
                                </el-form-item>
                                <el-form-item style="width:12%">
                                    <el-button type="primary" icon="el-icon-search" @click="attack_queue_query()">查询</el-button>
                                </el-form-item>
                            </el-form>
                        </el-col>
                        <el-col :span="8"  style="text-align: right">
                            <el-button  icon="el-icon-refresh" @click="attack_queue_query()">刷新</el-button>
                        </el-col>
                    </el-row>
                    <el-table :data="task_detail.attack_queue">
                        <el-table-column type="expand" >
                            <template slot-scope="props">
                                <el-form  class="demo-table-expand" label-width="auto">
                                    <el-form-item label="Webshell访问链接:" style="width:100%" v-if="props.row.webshell_url!=''">
                                        <span>{{ props.row.webshell_url }}</span>
                                    </el-form-item>
                                    <el-form-item label="Webshell访问密码:" style="width:100%" v-if="props.row.webshell_pass!=''">
                                        <span>{{ props.row.webshell_pass }}</span>
                                    </el-form-item>
                                    <el-form-item label="Webshell访问工具:" style="width:100%" v-if="props.row.webshell_access_tool!=''" >
                                        <span>{{ props.row.webshell_access_tool }}</span>
                                    </el-form-item>
                                    <el-form-item label="漏洞利用其他返回数据:" style="width:100%" v-if="props.row.remark!=''" >
                                        <span>{{ props.row.remark }}</span>
                                    </el-form-item>
                                    <el-form-item label="漏洞利用失败原因:" style="width:100%" v-if="props.row.error_info!=''">
                                        <span>{{ props.row.error_info }}</span>
                                    </el-form-item>
                                </el-form>
                            </template>
                        </el-table-column>
                        <el-table-column prop="target" label="目标" width="200"></el-table-column>
                        <el-table-column prop="name" label="漏洞名称" width="400"  ></el-table-column>
                        <el-table-column prop="cve" label="漏洞编号" width="200"></el-table-column>
                        <el-table-column prop="status" label="结果" >
                            <template slot-scope="scope">
                                <div v-if="scope.row.status==0">
                                    <el-tag type="danger">失败</el-tag>
                                </div>
                                <div v-if="scope.row.status==1">
                                    <el-tag type="success">成功</el-tag>
                                </div>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div class="pagination-bar" >
                        <el-pagination
                                @current-change="handle_attack_queue_current_change"
                                :current-page="task_detail.current_attack_queue_page"  layout="total, prev, pager, next"
                                :total=" task_detail.attack_queue_total" >
                        </el-pagination>
                    </div>
                </el-tab-pane>
                <!--<el-tab-pane label="打击成功" name="second">
                    <el-table :data="task_detail.attack_success_queue">
                        <el-table-column prop="target" label="目标" width="150"></el-table-column>
                        <el-table-column prop="webshell_url" label="资源访问链接" width="200" :show-overflow-tooltip="true"></el-table-column>
                        <el-table-column prop="webshell_pass" label="资源访问密码" :show-overflow-tooltip="true"></el-table-column>
                        <el-table-column prop="webshell_access_tool" label="资源访问工具" :show-overflow-tooltip="true"></el-table-column>
                        <el-table-column prop="remark" label="其他信息" :show-overflow-tooltip="true"></el-table-column>
                    </el-table>
                    <div class="pagination-bar">
                        <el-pagination
                                @current-change="handle_task_current_change"
                                :current-page="task_query.current_task_page"  layout="total, prev, pager, next"
                                :total=" task_query.tasks.total">
                        </el-pagination>
                    </div>
                </el-tab-pane>-->
            </el-tabs>
        </el-dialog>
        <el-dialog :visible.sync="dialog_visible" :title="title" v-if="dialog_visible" width="80%"  :close-on-click-modal="false">
            <el-steps :active="create_task_form.active" process-status="process" finish-status="success">
                <el-step title="任务" description="输入任务名称及描述">></el-step>
                <el-step title="目标" description="输入目标url或上传目标文件"></el-step>
                <el-step title="漏洞插件" description="选择漏洞插件">></el-step>
                <el-step title="执行" description="选择任务是否立刻执行"></el-step>
                <el-step title="完成" description="任务配置完成"></el-step>
            </el-steps>
            <el-divider></el-divider>
            <el-form :model="create_task_form" ref="task" :rules="create_task_rules"  label-width="150px">
                <div v-show="create_task_form.active == 0">
                    <el-form-item label="任务名称" prop="name" required>
                        <el-input v-model="create_task_form.name" placeholder="任务名称"></el-input>
                    </el-form-item>
                    <el-form-item label="任务描述" prop="desc" required>
                        <el-input v-model="create_task_form.desc" placeholder="任务描述"></el-input>
                    </el-form-item>
                </div>
                <div v-show="create_task_form.active == 1">
                    <el-form-item label="目标格式" required>
                        <el-radio-group v-model="create_task_form.radio" @change="task_url_format_change" >
                            <el-radio  label="1">列表</el-radio>
                            <el-radio  label="2">文件</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item v-show="create_task_form.radio=='1'"  ref="url_list" label="目标列表" prop="url_list" required>
                        <el-input v-model="create_task_form.url_list" type="textarea" :autosize="{ minRows: 5}" placeholder="http://127.0.0.1/
http://127.0.0.1:8080/
http://192.168.1.2:8080/
                        "></el-input>
                    </el-form-item>
                    <el-form-item v-show="create_task_form.radio=='2'"  label="目标文件"  required>
                        <el-upload class="upload-demo"   drag :file-list="create_task_form.file_list" list-type="text"  :before-upload="task_file_before_upload" :on-remove="task_file_on_remove" :limit="1"  action="" :multiple="false">
                            <i class="el-icon-upload"></i>
                            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                            <div class="el-upload__tip" slot="tip">只能上传txt文件，且不超过1M</div>
                        </el-upload>
                    </el-form-item>
                </div>
                <div v-show="create_task_form.active == 2">
                    <el-row>
                        <el-col :span="19">
                            <el-form :inline="true" :model="plugin_query">
                                <el-form-item>
                                    <el-input v-model="plugin_query.name" clearable placeholder="漏洞插件名称"></el-input>
                                </el-form-item>
                                <el-form-item style="width:10%">
                                <el-select v-model="plugin_query.vul_type_id" @change="plugin_search_by_vultype()" clearable placeholder="漏洞类型">
                                    <el-option v-for="item in plugin_query.vultype_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                                </el-select>
                                </el-form-item>
                                <el-form-item style="width:10%">
                                <el-select v-model="plugin_query.level_id" @change="plugin_search_by_level()" clearable placeholder="危害等级">
                                    <el-option v-for="item in plugin_query.level_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                                </el-select>
                                </el-form-item>
                                <el-form-item style="width:10%">
                                <el-select v-model="plugin_query.effect_id" @change="plugin_search_by_effect()" clearable placeholder="利用效果">
                                    <el-option v-for="item in plugin_query.effect_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                                </el-select>
                                </el-form-item>
                                <el-form-item style="width:10%">
                                <el-select v-model="plugin_query.application_id" @change="plugin_search_by_application()" clearable placeholder="应用名称">
                                    <el-option v-for="item in plugin_query.application_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                                </el-select>
                                </el-form-item>
                                <el-form-item style="width:10%"> 
                                <el-select v-model="plugin_query.category_id" @change="plugin_search_by_category()" clearable placeholder="应用归类">
                                    <el-option v-for="item in plugin_query.category_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                                </el-select>
                                </el-form-item>
                                <el-form-item style="width:10%">
                                    <el-button type="primary" icon="el-icon-search" @click="plugin_search()">查询</el-button>
                                </el-form-item>
                            </el-form>
                        </el-col>
                        <el-col :span="5"  style="text-align: right">
                            <el-button  icon="el-icon-refresh" @click="plugin_refresh()">刷新</el-button>
                        </el-col>
                    </el-row>
                    <el-table ref="plugin_tables" :data="plugin_query.plugins.data" highlight-current-row :row-key="get_row_keys" :expand-row-keys="plugin_query.expands" @expand-change="get_plugin_extend" @selection-change="handle_task_plugin_selection_change" v-loading="plugin_query.table_loading" style="width: 100%; margin-top: 20px">
                        <el-table-column type="selection" reserve-selection>
                        </el-table-column>
                        <el-table-column type="expand">
                            <template slot-scope="props">
                                <el-form v-if="props.row.extend" label-position="left" inline class="demo-table-expand">
                                    <el-form-item label="目标版本:"><span>{{ props.row.extend.affect_version }}</span></el-form-item>
                                    <el-form-item label=""><span></span></el-form-item>
                                    <el-form-item label="目标语言:"><span>{{ props.row.extend.language_name }}</span></el-form-item>
                                    <el-form-item label=""><span></span></el-form-item>
                                    <el-form-item label="目标系统:"><span>{{ props.row.extend.os }}</span></el-form-item>
                                    <el-form-item label=""><span></span></el-form-item>
                                    <el-form-item label="提交时间:"><span>{{ props.row.extend.enter_time }}</span></el-form-item>
                                    <el-form-item label=""><span></span></el-form-item>
                                    <el-form-item label="更新时间:"><span>{{ props.row.extend.update_time }}</span></el-form-item>
                                    <el-form-item label=""><span></span></el-form-item>
                                    <el-form-item label="漏洞描述:"><span>{{ props.row.extend.desc }}</span></el-form-item>
                                </el-form>
                            </template>
                        </el-table-column>

                        <el-table-column prop="exploit_name" label="漏洞名称"></el-table-column>
                        <el-table-column prop="cve" label="漏洞编号"></el-table-column>
                        <el-table-column prop="vultype_name" label="漏洞类型"></el-table-column>
                        <el-table-column prop="level_name" label="危害等级"></el-table-column>
                        <el-table-column prop="effect_name" label="利用效果"></el-table-column>
                        <el-table-column prop="application_name" label="应用名称"></el-table-column>
                        <el-table-column prop="category_name" label="应用归类"></el-table-column>
                        <el-table-column prop="author" label="提交者"></el-table-column>
                    </el-table>
                    <div class="pagination-bar" v-if="plugin_query.plugins.total > 10">
                        <el-pagination
                                @current-change="handle_plugin_current_change"
                                :current-page="plugin_query.current_plugin_page"  layout="total, prev, pager, next"
                                :total="plugin_query.plugins.total">
                        </el-pagination>
                    </div>
                </div>
                <div v-show="create_task_form.active == 3">
                    <el-form-item label="任务执行模式"  required>
                        <el-select v-model="create_task_form.exec_model.exec_model_id"  placeholder="任务执行模式">
                            <el-option v-for="item in create_task_form.exec_model.exec_model_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="立刻执行任务"  required>
                        <el-switch v-model="create_task_form.at_once" active-color="#13ce66"  active-text="启用" inactive-text="关闭"></el-switch>
                    </el-form-item>
                </div>
                <div v-show="create_task_form.active == 4">
                    
                </div>
            </el-form>
            <el-button v-if="create_task_form.active > 0" type="primary" style="margin-top: 12px"  icon="el-icon-back" @click="pre">上一步</el-button>
            <el-button v-if="create_task_form.active < 4" type="primary" style="margin-top: 12px" icon="el-icon-right" @click="next">下一步</el-button>
            <el-button v-if="create_task_form.active >= 4" type="primary" @click="task_commit" :loading="create_task_form.btnSaveLoading">提交</el-button>

        </el-dialog>
    </div>
</template>


<style>
    .demo-table-expand {
        font-size: 0;
    }
    .demo-table-expand label {
        width: 90px;
        color: #99a9bf;
    }
    .demo-table-expand .el-form-item {
        margin-right: 0;
        margin-bottom: 0;
        width: 50%;
    }
    .el-tooltip__popper {

        max-width: 800px;

    }
</style>

<script>
    export default {
        data () {
            return {
                dialog_task_detail_visible: false,
                task_detail:{
                    activeName: 'first',
                    current_task_id:0,
                    attack_queue: [
                        {
                            target: '127.0.0.1',
                            name: '王小虎',
                            cve: 'cve-1111-2222',
                            webshell_url:"https://192.168.2.101:8443/JCRikOXK.jsp",
                            webshell_pass:"rebeyond",
                            webshell_access_tool:"behinder",
                            remark:"最近的项目中使用到element-ui组件库，由于做的是后台管理系统，所以经常需要操作表格，编辑样式的过程中遇到一些问题，官网针对table给出了很多的api，自己可以自定义，基本能满足产品需求，但是没有给出具体的案例，网上的资料也比较简略，这里简单整理下一些常用的操作，如果有类似的功能可以做一个参考。\
具体的使用方法还是建议仔细阅读官网-table章节：",
                            status:"1",
                            error_info:""
                        }],
                    attack_queue_total:0,
                    attack_success_queue_total:0,
                    current_attack_queue_page: 1,
                    current_attack_success_queue_page: 1,
                    attack_success_queue:[
                        {
                            target: '127.0.0.1',
                            name: '王小虎',
                            cve: 'cve-1111-2222',
                            webshell_url:"https://192.168.2.101:8443/JCRikOXK.jsp",
                            webshell_pass:"rebeyond",
                            webshell_access_tool:"behinder",
                            status:"1"
                        }
                    ],
                    attack_queue_target:"",
                    attack_queue_status:"",
                    attack_queue_status_options:[
                        {"id":0,"name":"失败"},
                        {"id":1,"name":"成功"}
                    ]
                },
                task_query:{
                    name:"",
                    task_status:"",
                    btn_del_loading: false,
                    table_loading:false,
                    current_task_page: 1,
                    tasks:{},
                    status_options:[
                        {"id":0,"name":"未开始"},
                        {"id":1,"name":"运行中"},
                        {"id":2,"name":"已完成"}
                    ]

                },
                plugin_query: {
                    name: '',
                    vul_type_id: '',
                    level_id: '',
                    effect_id: '',
                    application_id: '',
                    category_id: '',
                    current_plugin_page: 1,
                    plugins: {},
                    vultype_options: [],
                    level_options: [],
                    effect_options: [],
                    application_options: [],
                    category_options: [],
                    language_options: [],
                    expands: [],
                    table_loading: false
                },
                dialog_visible: false,
                create_task_form: {
                    name:"",
                    active: 0,
                    desc:"",
                    at_once:false,
                    radio:"1",
                    url_list:"",
                    url_file:"",
                    file_list:[],
                    plugin_list:[],
                    exec_model:{
                        exec_model_id:1,
                        exec_model_options:[]
                    },
                    btnSaveLoading: false
                },
                create_task_rules: {
                    name: [
                        { required: true, message: '任务名称不能为空', trigger: ['blur','change'] }
                    ],
                    desc: [
                    { required: true, message: '任务描述不能为空', trigger: ['blur','change'] }
                    ],
                    url_list: [
                    { required: true, message: '目标列表不能为空', trigger: ['blur','change'] },
                    { pattern: /^((?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\*\+,;=.]+(\n)?)+$/, message: '请输入正确的目标列表', trigger: ['blur','change'] }
                    ]
                }
            }
        },
        methods: {
            task_delete(row){
                this.$confirm('此操作将永久删除该任务，是否继续？', '删除确认', {type: 'warning'}).then(() => {
                    this.task_query.btn_del_loading = true;
                    this.$http.delete(`/api/task/index/${row.id}`).then(
                        res => {
                            this.$layer_message(res.result.msg,"success");
                            this.task_search(this.task_query.current_task_page);
                        },
                        res => this.$layer_message(res.result)
                        ).finally(() => this.task_query.btn_del_loading = false)
                }).catch(() => {
                })
            },
            handle_attack_queue_current_change(val) {
                this.task_detail.current_attack_queue_page = val;
                this.attack_queue_query();
            },
            attack_queue_query() {
                let form={
                        target:this.task_detail.attack_queue_target,
                        task_id:this.task_detail.current_task_id,
                        status:this.task_detail.attack_queue_status
                    }
                this.task_detail.current_attack_queue_page = 1;
                this.$http.post("/api/task/detail/attack_queue/",{page: this.task_detail.current_attack_queue_page, attack_queue_query: form}).then(
                    res=>{
                        this.task_detail.attack_queue=res.result.attack_queue;
                        this.task_detail.attack_queue_total=res.result.total;
                        this.dialog_task_detail_visible=true;
                    },
                    res=>{
                        this.$layer_message(res.result);
                    }
                )
                
            },
            task_detail_query(row){
                this.task_detail.current_task_id=row.id;
                this.attack_queue_query();

            },
            task_refresh(){
                this.task_search(this.task_query.current_task_page);
            },
            task_start(row){
                this.$http.get(`/api/task/start/${row.id}`).then(
                    res=>{
                        this.$layer_message('任务启动成功', 'success');
                        
                    },
                    res=>{
                        this.$layer_message('任务启动失败');
                    }
                ).then(()=>{this.task_search(this.task_query.current_task_page);});
            },
            task_search_by_status(){
                this.task_query.current_task_page = 1;
                this.task_search();
            },
            handle_task_current_change(val) {
                this.task_query.current_task_page = val;
                this.task_search(this.task_query.current_task_page);
            },
            task_search(page){
                if (!page) this.task_query.current_task_page = 1;
                let form={
                    task_status:"",
                    name:""
                }
                form.task_status=this.task_query.task_status;
                form.name=this.task_query.name;
                this.task_query.table_loading = true;
                this.$http.post('/api/task/index', {page: this.task_query.current_task_page, task_query: form}).then(res => {
                    this.task_query.tasks = res.result
                }, res => this.$layer_message(res.result)).finally(() => this.task_query.table_loading = false)
            },
            handle_task_plugin_selection_change(val) {
            　　this.create_task_form.plugin_list = val;
            },
            task_file_on_remove(file, fileList) {
                this.create_task_form.url_file = "";
                this.create_task_form.file_list=[];
            },
            task_file_before_upload(file){
                let fd = new FormData();
                fd.append('url_file',file);
                this.$http.post("/api/task/file_upload",fd).then(
                    res =>{
                        this.create_task_form.url_file = file.name;
                        this.create_task_form.file_list=res.result.file_list;
                        this.$layer_message(res.result.status,"success");
                    },
                    res => this.$layer_message(res.result)
                )
                
                return false
            },
            task_url_format_change(){
                if(this.create_task_form.radio==1){
                    this.create_task_form.url_file = "";
                    this.create_task_form.file_list=[];
                }
                else if(this.create_task_form.radio==2){
                    this.$refs.url_list.resetField();
                }
                
            },
            next() {
                let is_next = true;
                if(this.create_task_form.active==0){
                    this.$refs.task.validateField(["name","desc"],(errormsg)=>{
                    if(!errormsg){
                        is_next = is_next &&true;
                    }
                    else{
                        is_next = is_next &&false;
                    }
                    });
                }
                if(this.create_task_form.active==1){
                    if(this.create_task_form.radio==1){
                        this.$refs.task.validateField(["url_list"],(errormsg)=>{
                        if(!errormsg){
                            is_next = is_next &&true;
                        }
                        else{
                            is_next = is_next &&false;
                        }
                        });
                    }
                    else if(this.create_task_form.radio==2){
                        if(this.create_task_form.url_file==""){
                            is_next = is_next &&false;
                            this.$layer_message("请上传目标文件");
                        }
                    }
                    else{

                    }
                }

                if(this.create_task_form.active==2){
                    if(this.create_task_form.plugin_list.length==0){
                        is_next = is_next &&false;
                        this.$layer_message("请选择合适的漏洞插件");

                    }
                }
                
                if (is_next && this.create_task_form.active++ > 4){
                    this.create_task_form.active = 5
                } 
            },
            pre() {
                if (this.create_task_form.active-- < 0) this.create_task_form.active = 0
                },
            plugin_refresh(){
                this.plugin_search(this.plugin_query.current_plugin_page);
            },
            get_row_keys(row) {
                    return row.id;
            },
            handle_plugin_current_change(val) {
                this.plugin_query.current_plugin_page = val;
                this.plugin_search(this.plugin_query.current_plugin_page);
            },
            plugin_search_by_vultype(){
                this.plugin_query.current_plugin_page = 1;
                this.plugin_search();
            },
            plugin_search_by_level(){
                this.plugin_query.current_plugin_page = 1;
                this.plugin_search();
            },
            plugin_search_by_effect(){
                this.plugin_query.current_plugin_page = 1;
                this.plugin_search();
            },
            plugin_search_by_application(){
                this.plugin_query.current_plugin_page = 1;
                this.plugin_search();
            },
            plugin_search_by_category(){
                this.plugin_query.current_plugin_page = 1;
                this.plugin_search();
            },
            get_plugin_vul_types() {
                this.$http.get('/api/exploit/vultypes').then(res => {
                    this.plugin_query.vultype_options = res.result.data
                }, res => this.$layer_message(res.result))
            },
            get_plugin_levels () {
                this.$http.get('/api/exploit/levels').then(res => {
                    this.plugin_query.level_options = res.result.data
                }, res => this.$layer_message(res.result))
            },
            get_plugin_effects () {
                this.$http.get('/api/exploit/effects').then(res => {
                    this.plugin_query.effect_options = res.result.data
                }, res => this.$layer_message(res.result))
            },
            get_plugin_applications () {
                this.$http.get('/api/exploit/applications').then(res => {
                    this.plugin_query.application_options = res.result.data
                }, res => this.$layer_message(res.result))
            },
            get_plugin_categories() {
                this.$http.get('/api/exploit/categories').then(res => {
                    this.plugin_query.category_options = res.result.data
                }, res => this.$layer_message(res.result))
            },
            get_plugin_aim_languages() {
                this.$http.get('/api/exploit/languages').then(res => {
                    this.plugin_query.language_options = res.result.data
                }, res => this.$layer_message(res.result))
            },
            plugin_search(page) {
                if (!page) this.plugin_query.current_plugin_page = 1;
                this.plugin_query.table_loading = true;
                this.plugin_query.expands=[];
                let api_uri = '/api/exploit/vulnerability/list';
                this.$http.post(api_uri, {page: this.plugin_query.current_plugin_page, plugin_query: this.plugin_query}).then(res => {
                    this.plugin_query.plugins = res.result
                }, res => this.$layer_message(res.result)).finally(() => this.plugin_query.table_loading = false)
            },
            get_plugin_extend (row, expanded) {
                if (expanded.length>0) {
                    this.plugin_query.expands = [];
                    this.plugin_query.expands.push(row.id);
                    this.$http.get(`/api/exploit/plugins/${row.id}/extend`).then(res => {
                        this.$set(row, 'extend', res.result);
                    }, res => this.$layer_message(res.result))
                }
                else{
                    this.plugin_query.expands = [];
                }
            },
            get_plugin_exec_models(){
                this.$http.get('/api/task/exec_models').then(
                    res => {
                        this.create_task_form.exec_model.exec_model_options = res.result.data;
                    },
                    res => {
                        this.$layer_message(res.result)
                })
            },
            handle_task_add () {
                this.create_task_form = {
                    name:"",
                    active: 0,
                    at_once:false,
                    radio:"1",
                    url_list:"",
                    url_file:"",
                    file_list:[],
                    plugin_list:[],
                    exec_model:{
                        exec_model_id:1,
                        exec_model_options:[]
                    },
                    btnSaveLoading: false
                };
                this.plugin_search();
                this.get_plugin_vul_types();
                this.get_plugin_levels ();
                this.get_plugin_effects();
                this.get_plugin_applications();
                this.get_plugin_categories();
                this.get_plugin_aim_languages();
                this.get_plugin_exec_models();
                this.title = '创建任务';
                this.dialog_visible = true;
                
            },
            task_edit(row){
                this.create_task_form = {
                    name:"",
                    active: 0,
                    desc:"",
                    at_once:false,
                    radio:"1",
                    url_list:"",
                    url_file:"",
                    file_list:[],
                    plugin_list:[],
                    exec_model:{
                        exec_model_id:1,
                        exec_model_options:[]
                    },
                    btnSaveLoading: false
                };
                this.plugin_search();
                this.get_plugin_vul_types();
                this.get_plugin_levels ();
                this.get_plugin_effects();
                this.get_plugin_applications();
                this.get_plugin_categories();
                this.get_plugin_aim_languages();
                this.get_plugin_exec_models();
                this.$http.get(`/api/task/edit/${row.id}`).then(res => {
                        this.create_task_form.id=res.result.id;
                        this.create_task_form.name = res.result.name;
                        if(res.result.url_list!=""){
                            this.create_task_form.url_list=res.result.url_list.replace(",","\n");
                        }
                        else{
                            let temp=res.result.url_file_path.split("_");
                            temp.shift();
                            let file_name=temp.join("_");
                            this.create_task_form.url_file=file_name;
                            this.create_task_form.file_list=[{name:file_name,path:res.result.url_file_path}]
                        }
                        this.create_task_form.exec_model.exec_model_id=res.result.exec_model_id;
                        this.create_task_form.desc=res.result.desc;
                        for(let i in res.result.plugins.split(","))
                            this.$refs.plugin_tables.toggleRowSelection(this.plugin_query.plugins.data[i],true);
                        
                    }, res => this.$layer_message(res.result))
                this.dialog_visible = true;
                this.title = '编辑任务';
            },
            task_commit () {
                this.create_task_form.btnSaveLoading = true;
                if (this.create_task_form.id) {
                    let form={
                        name:"",
                        url_list:"",
                        plugins:"",
                        desc:"",
                        url_file_path:"",
                        exec_model_id:1,
                        at_once:false
                    }
                    form.name=this.create_task_form.name;
                    let plugins=[];
                    for(let plugin of this.create_task_form.plugin_list){
                        plugins.push(plugin.id);
                    }
                    form.plugins=plugins.join(",");
                    form.desc=this.create_task_form.desc;
                    if(this.create_task_form.url_list!=""){
                        let urls=Array.from(new Set(this.create_task_form.url_list.split("\n")));
                        form.url_list=urls.join(",");
                        form.url_file_path="";
                    }
                    else{
                        form.url_list="";
                        form.url_file_path=this.create_task_form.file_list[0].path;
                    }
                    form.exec_model_id=this.create_task_form.exec_model.exec_model_id;
                    this.$http.put(`/api/task/edit/${this.create_task_form.id}`,form).then(
                        res=>{
                            console.log("success");
                            if(this.create_task_form.at_once){
                                this.$http.get(`/api/task/start/${res.result.id}`).then(
                                    res=>{
                                        this.create_task_form.btnSaveLoading = false;
                                        this.$layer_message('更新任务成功并启动任务', 'success');
                                        this.dialog_visible = false;
                                    },
                                    res=>{
                                        this.create_task_form.btnSaveLoading = false;
                                        this.$layer_message('更新任务成功,但任务未启动');
                                        this.dialog_visible = false;
                                    }
                                );
                            }
                            else{
                                this.create_task_form.btnSaveLoading = false;
                                this.$layer_message('更新任务成功','success');
                                this.dialog_visible = false;
                            }
                        },
                        res=>{
                            console.log("fail");
                            this.$layer_message(res.result);
                            this.create_task_form.btnSaveLoading = false;
                        }
                        
                    )
                    this.task_search(this.task_query.current_task_page);
                    
                } 
                else {
                   let form={
                        name:"",
                        url_list:"",
                        plugins:"",
                        desc:"",
                        url_file_path:"",
                        exec_model_id:1,
                        at_once:false
                    }
                    form.name=this.create_task_form.name;
                    let plugins=[];
                    for(let plugin of this.create_task_form.plugin_list){
                        plugins.push(plugin.id);
                    }
                    form.plugins=plugins.join(",");
                    form.desc=this.create_task_form.desc;
                    if(this.create_task_form.url_list!=""){
                        let urls=Array.from(new Set(this.create_task_form.url_list.split("\n")));
                        form.url_list=urls.join(",");
                        form.url_file_path="";
                    }
                    else{
                        form.url_list="";
                        form.url_file_path=this.create_task_form.file_list[0].path;
                    }
                    form.exec_model_id=this.create_task_form.exec_model.exec_model_id;
                    this.$http.post('/api/task/add', form).then(
                        res => {
                            if(this.create_task_form.at_once){
                                this.$http.get(`/api/task/start/${res.result.id}`).then(
                                    res=>{
                                        this.create_task_form.btnSaveLoading = false;
                                        this.$layer_message('创建任务成功并启动任务', 'success');
                                        this.dialog_visible = false;
                                    },
                                    res=>{
                                        this.create_task_form.btnSaveLoading = false;
                                        this.$layer_message('创建任务成功,但任务未启动');
                                        this.dialog_visible = false;
                                    }
                                );
                            }
                            else{
                                this.create_task_form.btnSaveLoading = false;
                                this.$layer_message('创建任务成功','success');
                                this.dialog_visible = false;
                            }
                            this.task_search();
                    }, res =>{
                        this.$layer_message(res.result);
                        this.create_task_form.btnSaveLoading = false;
                    });
                    
                }
                
            },
            deleteCommit (row) {
                this.$confirm('此操作将永久删除该漏洞插件，是否继续？', '删除确认', {type: 'warning'}).then(() => {
                    this.btnDelLoading = {[row.id]: true};
                    this.$http.delete(`/api/exploit/plugins/${row.id}`).then(() => {
                        this.search(this.currentPage)
                    }, res => this.$layer_message(res.result)).finally(() => this.btnDelLoading = {})
                }).catch(() => {
                })
            }

        },
        created () {
            this.task_search();
        }
    }
</script>
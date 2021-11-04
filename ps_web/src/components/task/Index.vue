<template>
    <div>
        <el-row>
            <el-col :span="19">
                <el-form :inline="true" :model="plugin_query">
                    <el-form-item>
                        <el-input v-model="plugin_query.name" clearable placeholder="任务名称"></el-input>
                    </el-form-item>
                    <!--<el-form-item style="width:12%">
                    <el-select v-model="plugin_query.vul_type_id" @change="search_by_vultype()" clearable placeholder="漏洞类型">
                        <el-option v-for="item in vultype_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                    </el-select>
                    </el-form-item>
                    <el-form-item style="width:12%">
                    <el-select v-model="plugin_query.level_id" @change="search_by_level()" clearable placeholder="危害等级">
                        <el-option v-for="item in level_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                    </el-select>
                    </el-form-item>
                    <el-form-item style="width:12%">
                    <el-select v-model="plugin_query.effect_id" @change="search_by_effect()" clearable placeholder="利用效果">
                        <el-option v-for="item in effect_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                    </el-select>
                    </el-form-item>
                    <el-form-item style="width:12%">
                    <el-select v-model="plugin_query.application_id" @change="search_by_application()" clearable placeholder="应用名称">
                        <el-option v-for="item in application_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                    </el-select>
                    </el-form-item>
                    <el-form-item style="width:12%"> 
                    <el-select v-model="plugin_query.category_id" @change="search_by_category()" clearable placeholder="应用归类">
                        <el-option v-for="item in category_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                    </el-select>
                    </el-form-item>-->
                    <el-form-item style="width:12%">
                        <el-button type="primary" icon="el-icon-search" @click="search()">查询</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
            <el-col :span="5"  style="text-align: right">
                <el-button  icon="el-icon-refresh" @click="refresh()">刷新</el-button>
                <el-button v-if="has_permission('exploit_plugin_add')" type="primary" icon="el-icon-plus" @click="handle_task_add">新建任务</el-button>
            </el-col>
        </el-row>
        <el-row></el-row>
        <el-table :data="plugins.data" highlight-current-row :row-key="getRowKeys" :expand-row-keys="expands" @expand-change="get_plugin_extend" v-loading="tableLoading" style="width: 100%; margin-top: 20px">
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
                   <!-- <el-row v-else style="text-align: center">
                        <span style="color: #99a9bf">暂没有额外信息</span>
                    </el-row>-->
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
            <el-table-column label="操作" width="270px" v-if="has_permission('assets_host_edit|assets_host_del|assets_host_valid')">
                <template slot-scope="scope">
                    <el-button v-if="has_permission('assets_host_edit')" size="small" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
                    <el-button v-if="has_permission('assets_host_valid')" size="small" type="primary" @click="valid(scope.row)"
                               :loading="btnValidLoading[scope.row.id]">验证
                    </el-button>
                    <el-button v-if="has_permission('assets_host_del')" size="small" icon="el-icon-delete" type="danger" @click="deleteCommit(scope.row)"
                               :loading="btnDelLoading[scope.row.id]">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <!--分页-->
        <div class="pagination-bar" v-if="plugins.total > 10">
            <el-pagination
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"  layout="total, prev, pager, next"
                    :total="plugins.total">
            </el-pagination>
        </div>

        <el-dialog :visible.sync="dialogVisible" :title="title" v-if="dialogVisible" width="80%"  :close-on-click-modal="false">
            <el-steps :active="active" process-status="process" finish-status="success">
                <el-step title="任务" description="输入任务名称及描述">></el-step>
                <el-step title="目标" description="输入目标url或上传目标文件"></el-step>
                <el-step title="漏洞插件" description="选择漏洞插件">></el-step>
                <el-step title="执行" description="选择任务是否立刻执行"></el-step>
                <el-step title="完成" description="任务配置完成"></el-step>
            </el-steps>
            <el-divider></el-divider>
            <el-form :model="form" label-width="150px">
                <div v-show="active == 0">
                    <el-form-item label="任务名称" prop="name" required>
                        <el-input v-model="form.name" placeholder="任务名称"></el-input>
                    </el-form-item>
                    <el-form-item label="任务描述" prop="desc" required>
                        <el-input v-model="form.desc" placeholder="任务描述"></el-input>
                    </el-form-item>
                </div>
                <div v-show="active == 1">
                    <el-form-item label="目标格式" required>
                        <el-radio v-model="radio" label="1">列表</el-radio>
                        <el-radio v-model="radio" label="2">文件</el-radio>
                    </el-form-item>
                    <el-form-item v-if="radio=='1'" label="目标列表" prop="url_list" required>
                        <el-input v-model="form.url_list" type="textarea" :autosize="{ minRows: 5}" placeholder="http://127.0.0.1/
http://127.0.0.1:8080/
http://192.168.1.2:8080/
                        "></el-input>
                    </el-form-item>
                    <el-form-item v-if="radio=='2'" label="目标文件" prop="url_file" required>
                        <el-upload class="upload-demo" drag action="" multiple>
                            <i class="el-icon-upload"></i>
                            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                            <div class="el-upload__tip" slot="tip">只能上传txt文件，且不超过1M</div>
                        </el-upload>
                    </el-form-item>
                </div>
                <div v-show="active == 2">
                    <el-row>
                        <el-col :span="19">
                            <el-form :inline="true" :model="plugin_query">
                                <el-form-item>
                                    <el-input v-model="plugin_query.name" clearable placeholder="漏洞插件名称"></el-input>
                                </el-form-item>
                                <el-form-item style="width:10%">
                                <el-select v-model="plugin_query.vul_type_id" @change="search_by_vultype()" clearable placeholder="漏洞类型">
                                    <el-option v-for="item in vultype_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                                </el-select>
                                </el-form-item>
                                <el-form-item style="width:10%">
                                <el-select v-model="plugin_query.level_id" @change="search_by_level()" clearable placeholder="危害等级">
                                    <el-option v-for="item in level_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                                </el-select>
                                </el-form-item>
                                <el-form-item style="width:10%">
                                <el-select v-model="plugin_query.effect_id" @change="search_by_effect()" clearable placeholder="利用效果">
                                    <el-option v-for="item in effect_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                                </el-select>
                                </el-form-item>
                                <el-form-item style="width:10%">
                                <el-select v-model="plugin_query.application_id" @change="search_by_application()" clearable placeholder="应用名称">
                                    <el-option v-for="item in application_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                                </el-select>
                                </el-form-item>
                                <el-form-item style="width:10%"> 
                                <el-select v-model="plugin_query.category_id" @change="search_by_category()" clearable placeholder="应用归类">
                                    <el-option v-for="item in category_options" :label="item.name" :key="item.id" :value="item.id"></el-option>
                                </el-select>
                                </el-form-item>
                                <el-form-item style="width:10%">
                                    <el-button type="primary" icon="el-icon-search" @click="search()">查询</el-button>
                                </el-form-item>
                            </el-form>
                        </el-col>
                        <el-col :span="5"  style="text-align: right">
                            <el-button  icon="el-icon-refresh" @click="refresh()">刷新</el-button>
                            <!--<el-button v-if="has_permission('exploit_plugin_add')" type="primary" icon="el-icon-plus" @click="handle_task_add">新建任务</el-button>-->
                        </el-col>
                    </el-row>
                    <el-table ref="multipleTable" :data="plugins.data" highlight-current-row :row-key="getRowKeys" :expand-row-keys="expands" @expand-change="get_plugin_extend" v-loading="tableLoading" style="width: 100%; margin-top: 20px">
                        <el-table-column type="selection">
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
                            <!-- <el-row v-else style="text-align: center">
                                    <span style="color: #99a9bf">暂没有额外信息</span>
                                </el-row>-->
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
                        <el-table-column label="操作" width="270px" v-if="has_permission('assets_host_edit|assets_host_del|assets_host_valid')">
                            <template slot-scope="scope">
                                <el-button v-if="has_permission('assets_host_edit')" size="small" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
                                <el-button v-if="has_permission('assets_host_del')" size="small" icon="el-icon-delete" type="danger" @click="deleteCommit(scope.row)"
                                        :loading="btnDelLoading[scope.row.id]">删除
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>

                    <!--分页-->
                    <div class="pagination-bar" v-if="plugins.total > 10">
                        <el-pagination
                                @current-change="handleCurrentChange"
                                :current-page="currentPage"  layout="total, prev, pager, next"
                                :total="plugins.total">
                        </el-pagination>
                    </div>
                </div>
                <div v-show="active == 3">
                    <el-form-item label="立刻执行任务"  required>
                        <el-switch v-model="at_once" active-color="#13ce66"  active-text="启用" inactive-text="关闭"></el-switch>
                    </el-form-item>
                </div>
                <div v-show="active == 4">
                    
                </div>
            </el-form>
            <el-button v-if="active > 0" type="primary" style="margin-top: 12px"  icon="el-icon-back" @click="pre">上一步</el-button>
            <el-button v-if="active < 4" type="primary" style="margin-top: 12px" icon="el-icon-right" @click="next">下一步</el-button>
            <el-button v-if="active >= 4" type="primary" @click="task_commit" :loading="btnSaveLoading">创建任务</el-button>
            
            <!--<div slot="footer">
                <el-button @click="dialogVisible=false">取消</el-button>
                <el-button type="primary" @click="task_commit" :loading="btnSaveLoading">创建</el-button>
            </div>-->
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
</style>

<script>
    export default {
        data () {
            return {
                active: 0,
                radio:"1",
                at_once:false,
                plugin_query: {
                    name: '',
                    vul_type_id: '',
                    level_id: '',
                    effect_id: '',
                    application_id: '',
                    category_id: ''
                },
                dialogVisible: false,
                btnSaveLoading: false,
                btnDelLoading: {},
                btnValidLoading: {},
                tableLoading: true,
                form: {},
                plugins: {},
                currentPage: 1,
                vultype_options: [],
                level_options: [],
                effect_options: [],
                application_options: [],
                category_options: [],
                language_options: [],
                expands: []
            }
        },
        methods: {
            next() {
                if (this.active++ > 4)this.active = 5
                },
                // 步骤条上一步的方法
            pre() {
                if (this.active-- < 0) this.active = 0
                },
             //刷新
            refresh(){
                this.search(this.currentPage);
            },
            getRowKeys(row) {
                    return row.id;
            },
            handleCurrentChange(val) {
                this.currentPage = val;
                this.search(this.currentPage);
            },

            //漏洞类型查询
            search_by_vultype(){
                this.currentPage = 1;
                this.search();
            },

            //危害等级查询
            search_by_level(){
                this.currentPage = 1;
                this.search();
            },

            //利用效果查询
            search_by_effect(){
                this.currentPage = 1;
                this.search();
            },

            //应用名称查询
            search_by_application(){
                this.currentPage = 1;
                this.search();
            },

            //应用归类查询
            search_by_category(){
                this.currentPage = 1;
                this.search();
            },

            //获取漏洞类型
            get_vul_types () {
                this.$http.get('/api/exploit/vultypes').then(res => {
                    this.vultype_options = res.result.data
                }, res => this.$layer_message(res.result))
            },

            //获取危害等级
            get_levels () {
                this.$http.get('/api/exploit/levels').then(res => {
                    this.level_options = res.result.data
                }, res => this.$layer_message(res.result))
            },
            //获取利用效果
            get_effects () {
                this.$http.get('/api/exploit/effects').then(res => {
                    this.effect_options = res.result.data
                }, res => this.$layer_message(res.result))
            },

            //获取应用名称
            get_applications () {
                this.$http.get('/api/exploit/applications').then(res => {
                    this.application_options = res.result.data
                }, res => this.$layer_message(res.result))
            },

            //获取应用归类
            get_categories () {
                this.$http.get('/api/exploit/categories').then(res => {
                    this.category_options = res.result.data
                }, res => this.$layer_message(res.result))
            },

            //获取语言种类
            get_languages () {
                this.$http.get('/api/exploit/languages').then(res => {
                    this.language_options = res.result.data
                }, res => this.$layer_message(res.result))
            },

            search (page) {
                if (!page) this.currentPage = 1;
                this.tableLoading = true;
                this.expands=[];
                let api_uri = '/api/exploit/plugins';
                this.$http.get(api_uri, {params: {page: this.currentPage, plugin_query: this.plugin_query}}).then(res => {
                    this.plugins = res.result
                }, res => this.$layer_message(res.result)).finally(() => this.tableLoading = false)
            },

            get_plugin_extend (row, expanded) {
                if (expanded.length>0) {
                    this.expands = [];
                    this.expands.push(row.id);
                    this.$http.get(`/api/exploit/plugins/${row.id}/extend`).then(res => {
                        this.$set(row, 'extend', res.result);
                    }, res => this.$layer_message(res.result))
                }
                else{
                    this.expands = [];
                }
            },

            handle_task_add () {
                this.form = {};
                this.title = '创建任务';
                this.dialogVisible = true;
                //this.importStatus = true;
            },

            handleEdit (row) {
                this.$http.get(`/api/exploit/plugins/${row.id}`).then(res => {
                        this.form = res.result;
                    }, res => this.$layer_message(res.result))
                this.dialogVisible = true;
                this.title = '编辑漏洞插件';
                //this.importStatus = false;
            },
            task_commit () {
                this.btnSaveLoading = true;
                let request;
                if (this.form.id) {
                    request = this.$http.put(`/api/task/index/${this.form.id}`, this.form)
                } else {
                    request = this.$http.post(`/api/task/index`, this.form)
                }
                request.then(() => {
                    this.dialogVisible = false;
                    this.$layer_message('提交成功', 'success');
                    this.search(this.currentPage);
                    this.expands=[];
                    /*this.get_vul_types();
                    this.get_levels ();
                    this.get_effects();
                    this.get_applications();
                    this.get_categories();
                    this.get_languages();*/
                }, res => this.$layer_message(res.result)).finally(() => this.btnSaveLoading = false)
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
            this.search();
            this.get_vul_types();
            this.get_levels ();
            this.get_effects();
            this.get_applications();
            this.get_categories();
            this.get_languages();
        }
    }
</script>
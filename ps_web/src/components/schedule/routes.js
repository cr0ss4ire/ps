/**
 * Created by zyupo on 2017/04/20.
 * https://github.com/openspug/spug
 */
import Job from './Job.vue'

export default [
    {
        path: 'job',
        component: Job,
        meta: {
            permission: 'job_task_view'
        }
    }
]
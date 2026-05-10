import { MOCK_RECORDS, MOCK_STATS } from './mockData';

var DELAY = 400;
var nextId = 31;

function wait(ms) {
    return new Promise(function(resolve) {
        setTimeout(resolve, ms);
    });
}

export async function login(email, password) {
    await wait(DELAY);
    if (!email || !password) {
        throw new Error('Email and password required');
    }
    var role = 'VIEWER';
    if (email.indexOf('admin') !== -1) {
        role = 'ADMIN';
    } else if (email.indexOf('manager') !== -1) {
        role = 'MANAGER';
    }
    return {
        token: 'mock-jwt-' + Date.now(),
        user: {
            id: 1,
            name: email.split('@')[0],
            email: email,
            role: role
        }
    };
}

export async function getRecords(opts) {
    if (!opts) opts = {};
    var page = opts.page || 0;
    var size = opts.size || 10;
    var search = opts.search || '';
    var status = opts.status || '';
    var sortBy = opts.sortBy || 'createdAt';
    var sortDir = opts.sortDir || 'desc';

    await wait(DELAY);

    var list = MOCK_RECORDS.slice();

    if (search) {
        var q = search.toLowerCase();
        list = list.filter(function(r) {
            return (
                r.title.toLowerCase().indexOf(q) !== -1 ||
                r.description.toLowerCase().indexOf(q) !== -1 ||
                r.assignedTo.toLowerCase().indexOf(q) !== -1 ||
                r.category.toLowerCase().indexOf(q) !== -1
            );
        });
    }

    if (status) {
        list = list.filter(function(r) {
            return r.status === status;
        });
    }

    list.sort(function(a, b) {
        var av = a[sortBy] || '';
        var bv = b[sortBy] || '';
        if (sortDir === 'asc') {
            return av > bv ? 1 : -1;
        }
        return av < bv ? 1 : -1;
    });

    var total = list.length;
    var start = page * size;
    var end = start + size;
    var content = list.slice(start, end);

    return {
        content: content,
        totalElements: total,
        totalPages: Math.ceil(total / size),
        number: page,
        size: size
    };
}

export async function getRecordById(id) {
    await wait(DELAY);
    var found = null;
    for (var i = 0; i < MOCK_RECORDS.length; i++) {
        if (MOCK_RECORDS[i].id === Number(id)) {
            found = MOCK_RECORDS[i];
            break;
        }
    }
    if (!found) {
        throw new Error('Record not found');
    }
    return found;
}

export async function createRecord(data) {
    await wait(DELAY + 200);
    var now = new Date().toISOString();
    var rec = {
        id: nextId++,
        title: data.title || '',
        category: data.category || '',
        status: data.status || 'Active',
        priority: data.priority || 'Medium',
        assignedTo: data.assignedTo || '',
        dueDate: data.dueDate || '',
        description: data.description || '',
        score: Math.floor(Math.random() * 30 + 60),
        createdAt: now,
        updatedAt: now,
        aiAnalysis: 'AI analysis pending...',
        tags: []
    };
    MOCK_RECORDS.unshift(rec);
    return rec;
}

export async function updateRecord(id, data) {
    await wait(DELAY);
    var idx = -1;
    for (var i = 0; i < MOCK_RECORDS.length; i++) {
        if (MOCK_RECORDS[i].id === Number(id)) {
            idx = i;
            break;
        }
    }
    if (idx === -1) {
        throw new Error('Record not found');
    }
    var old = MOCK_RECORDS[idx];
    MOCK_RECORDS[idx] = {
        id: old.id,
        title: data.title !== undefined ? data.title : old.title,
        category: data.category !== undefined ? data.category : old.category,
        status: data.status !== undefined ? data.status : old.status,
        priority: data.priority !== undefined ? data.priority : old.priority,
        assignedTo: data.assignedTo !== undefined ? data.assignedTo : old.assignedTo,
        dueDate: data.dueDate !== undefined ? data.dueDate : old.dueDate,
        description: data.description !== undefined ? data.description : old.description,
        score: old.score,
        createdAt: old.createdAt,
        updatedAt: new Date().toISOString(),
        aiAnalysis: old.aiAnalysis,
        tags: old.tags
    };
    return MOCK_RECORDS[idx];
}

export async function deleteRecord(id) {
    await wait(DELAY);
    for (var i = 0; i < MOCK_RECORDS.length; i++) {
        if (MOCK_RECORDS[i].id === Number(id)) {
            MOCK_RECORDS[i].status = 'Archived';
            MOCK_RECORDS[i].updatedAt = new Date().toISOString();
            return { message: 'Deleted' };
        }
    }
    throw new Error('Record not found');
}

export async function getStats() {
    await wait(DELAY);
    return MOCK_STATS;
}

export async function exportCSV(filters) {
    if (!filters) filters = {};
    await wait(300);
    var list = MOCK_RECORDS.slice();
    if (filters.status) {
        list = list.filter(function(r) {
            return r.status === filters.status;
        });
    }
    var lines = ['ID,Title,Category,Status,Priority,Score,Assigned To,Due Date,Created At'];
    for (var i = 0; i < list.length; i++) {
        var r = list[i];
        var created = r.createdAt ? r.createdAt.split('T')[0] : '';
        lines.push([
            r.id,
            '"' + r.title + '"',
            r.category,
            r.status,
            r.priority,
            r.score,
            '"' + r.assignedTo + '"',
            r.dueDate,
            created
        ].join(','));
    }
    var csv = lines.join('\n');
    var blob = new Blob([csv], { type: 'text/csv' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'records-' + Date.now() + '.csv';
    a.click();
    URL.revokeObjectURL(url);
}

export async function getAiRecommendations(recordId) {
    await wait(1200);
    var title = 'this record';
    var priority = 'Medium';
    var assignedTo = 'the assignee';
    for (var i = 0; i < MOCK_RECORDS.length; i++) {
        if (MOCK_RECORDS[i].id === Number(recordId)) {
            title = MOCK_RECORDS[i].title;
            priority = MOCK_RECORDS[i].priority;
            assignedTo = MOCK_RECORDS[i].assignedTo;
            break;
        }
    }
    return {
        recommendations: [{
                action_type: 'Prioritise',
                description: 'Schedule a focused sprint for this item given its ' + priority + ' priority.',
                priority: 'HIGH'
            },
            {
                action_type: 'Assign',
                description: 'Ensure ' + assignedTo + ' has unblocked time this week to drive progress.',
                priority: 'MEDIUM'
            },
            {
                action_type: 'Review',
                description: 'Set a checkpoint at 50% progress to catch blockers early.',
                priority: 'LOW'
            }
        ],
        meta: {
            model_used: 'llama-3.3-70b',
            confidence: 0.87,
            response_time_ms: 1183,
            cached: false
        }
    };
}

export async function getAuditLog(recordId) {
    await wait(DELAY);
    var createdAt = new Date().toISOString();
    var currentStatus = 'Active';
    for (var i = 0; i < MOCK_RECORDS.length; i++) {
        if (MOCK_RECORDS[i].id === Number(recordId)) {
            createdAt = MOCK_RECORDS[i].createdAt;
            currentStatus = MOCK_RECORDS[i].status;
            break;
        }
    }
    return [{
            id: 1,
            action: 'CREATE',
            performedBy: 'system',
            oldValue: null,
            newValue: 'Record created',
            timestamp: createdAt
        },
        {
            id: 2,
            action: 'UPDATE',
            performedBy: 'Arjun Mehta',
            oldValue: 'Not Started',
            newValue: 'In Progress',
            timestamp: new Date(Date.now() - 86400000).toISOString()
        },
        {
            id: 3,
            action: 'UPDATE',
            performedBy: 'Priya Sharma',
            oldValue: 'In Progress',
            newValue: currentStatus,
            timestamp: new Date(Date.now() - 3600000).toISOString()
        }
    ];
}
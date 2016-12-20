import {
  Map,
  fromJS
} from 'immutable'

const arrayToObj = (a) => a.reduce((acc, x) => {
  acc[x.id] = x;
  return acc
}, {})

const routinesMap = (routines) => {
  var rds = arrayToObj(routines.map(r => {
    r['routinedays'] = arrayToObj(r.routinedays.map(rd => {
      rd['routinedayslots'] = arrayToObj(rd.routinedayslots);
      return rd
    }));
    return r
  }))

  return fromJS(rds)
}

const convertRoutine = (routine) => {
  routine['routinedays'] = Map({})
  return Map(routine)
}

const convertRoutineday = (routineday) => {
  routineday['routinedayslots'] = Map({})
  return Map(routineday)
}

const routines = (state = Map({
  isFetching: false,
  routines: Map(),
}), action) => {
  switch (action.type) {
    case 'ROUTINES_REQUEST':
      return state.set('isFetching', true)
    case 'ROUTINES_REQUEST_FAILURE':
      return state.set('isFetching', false)
    case 'ROUTINES_SUCCESS':
      return state.set('isFetching', false)
        .set('routines', routinesMap(action.response))
    case 'ROUTINE_ADDED':
      {
        return state.setIn(['routines', action.response.id.toString()],
          convertRoutine(action.response))
      }
    case 'ROUTINE_RENAMED':
      return state.setIn(['routines', action.response.id.toString(), 'name'],
        action.response.name)
    case 'ROUTINE_DELETED':
      {
        return state.deleteIn(['routines', action.id.toString()])
      }
    case 'ROUTINEDAY_ADDED':
      {
        return state.setIn(
          ['routines',
            action.json.routine.toString(),
            'routinedays',
            action.json.id.toString()
          ],
          convertRoutineday(action.json)
        )
      }
    case 'ROUTINEDAY_DELETED':
      {

        return state.deleteIn(['routines', action.routine.toString(), 'routinedays', action.routineday.toString()])
      }
  case 'ROUTINEDAY_RENAMED':
    return state.setIn(['routines',
                        action.response.routine.toString(),
                        'routinedays',
                        action.response.id.toString(),
                        'name'
                        ],
                       action.response.name)
  case 'ROUTINEDAYSLOT_DELETED':
    return state.deleteIn(['routines',
                            action.routine.toString(),
                            'routinedays',
                            action.routineday.toString(),
                            'routinedayslots',
                            action.id.toString()
                          ])
  case 'ROUTINEDAYSLOT_ADDED':
    {
      return state.setIn(
        ['routines',
         action.routine.toString(),
         'routinedays',
         action.json.routineday.toString(),
         'routinedayslots',
         action.json.id.toString()
        ],
        Map(action.json)
      )
    }
    default:
      return state
  }
}

export default routines

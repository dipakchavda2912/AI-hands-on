import React, { useState } from 'react';
import './Timeline.css';

const Timeline = () => {
  const [currentTaskIndex, setCurrentTaskIndex] = useState(-1);
  const [selectedTaskIndex, setSelectedTaskIndex] = useState(-1);
  const [isRunning, setIsRunning] = useState(false);
  const [subtaskStatuses, setSubtaskStatuses] = useState({});

  const tasks = [
    {
      name: "Start of Evaluation",
      shortName: "Evaluation",
      description: "Preparation",
      note: null,
      subtasks: [
        "Initial planning",
        "Team assembly",
        "Resource allocation"
      ]
    },
    {
      name: "Initial Scoping",
      shortName: "Scoping",
      description: "Data checking",

      subtasks: [
        "Requirement gathering",
        "Scope definition",
        "Timeline planning",
        "Stakeholder approval"
      ]
    },
    {
      name: "Validation",
      shortName: "Validation",
      description: "Completed proof\nof concept",
      note: null,
      subtasks: [
        "Testing framework setup",
        "Unit testing",
        "Integration testing"
      ]
    },
    {
      name: "Contracting",
      shortName: "Contract",
      description: "Signed Contract",
      note: null,
      subtasks: [
        "Contract drafting",
        "Legal review",
        "Signature collection"
      ]
    },
    {
      name: "Migration",
      shortName: "Migration",
      description: "All information\nis migrated",
      note: {},
      subtasks: [
        "Data extraction",
        "Data transformation",
        "Data loading",
        "Verification"
      ]
    },
    {
      name: "Global Launch",
      shortName: "Launch",
      description: "In Asia, Australia,\nLatin America",
      note: null,
      subtasks: [
        "Pre-launch checklist",
        "Deployment",
        "Monitoring setup"
      ]
    }
  ];

  const totalSubtasks = tasks.reduce((sum, task) => sum + task.subtasks.length, 0);
  const completedSubtasksCount = Object.values(subtaskStatuses).filter(s => s === 'completed').length;
  const progressPercent = (completedSubtasksCount / totalSubtasks) * 100;

  const getStatusClass = (index) => {
    if (index < currentTaskIndex) return 'completed';
    if (index === currentTaskIndex) return 'active';
    return 'pending';
  };

  const getProgressLineWidth = () => {
    if (currentTaskIndex < 0) return '0%';
    if (currentTaskIndex >= tasks.length) return '100%';
    const progress = ((currentTaskIndex + 1) / tasks.length) * 100;
    return `${Math.min(progress, 100)}%`;
  };

  const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

  const startExecution = async () => {
    setIsRunning(true);
    setCurrentTaskIndex(-1);
    setSelectedTaskIndex(-1);
    setSubtaskStatuses({});

    for (let taskIdx = 0; taskIdx < tasks.length; taskIdx++) {
      setCurrentTaskIndex(taskIdx);
      setSelectedTaskIndex(taskIdx);

      for (let subtaskIdx = 0; subtaskIdx < tasks[taskIdx].subtasks.length; subtaskIdx++) {
        const key = `${taskIdx}-${subtaskIdx}`;

        // Set active
        setSubtaskStatuses(prev => ({ ...prev, [key]: 'active' }));
        await sleep(500);

        // Random error (10% chance)
        if (Math.random() < 0.1) {
          setSubtaskStatuses(prev => ({ ...prev, [key]: 'error' }));
          await sleep(300);
        }

        // Set completed
        setSubtaskStatuses(prev => ({ ...prev, [key]: 'completed' }));
      }
    }

    setCurrentTaskIndex(tasks.length);
    setSelectedTaskIndex(-1);
    setIsRunning(false);
  };

  const handleMilestoneClick = (index) => {
    // Only allow selection of completed or active tasks, not pending tasks
    const status = getStatusClass(index);
    if (status !== 'pending') {
      setSelectedTaskIndex(index);
    }
  };

  const getSubtaskStatus = (taskIdx, subtaskIdx) => {
    return subtaskStatuses[`${taskIdx}-${subtaskIdx}`] || 'pending';
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return '✅';
      case 'active': return '⏳';
      case 'error': return '❌';
      default: return '⚪';
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed': return { text: 'DONE', class: 'completed' };
      case 'active': return { text: 'PROCESSING', class: 'active' };
      case 'error': return { text: 'ERROR', class: 'error' };
      default: return { text: 'PENDING', class: 'pending' };
    }
  };

  return (
    <div className="timeline-app">
      {/* Header */}
      <header className="app-header">
        {/* <h1>📅 Timeline for Accord</h1> */}
        <p>Project Timeline & Progress Tracker</p>
      </header>

      {/* Controls */}
      <div className="controls">
        <button
          className="start-button"
          onClick={startExecution}
          disabled={isRunning}
        >
          {isRunning ? '⏳ Running...' : '▶️ Start Execution'}
        </button>
      </div>

      {/* Timeline Section */}
      <div className="timeline-wrapper">
        {/* <h2 className="timeline-header">Timeline for Accord</h2> */}

        <div className="timeline-container">
          {/* Progress Line */}
          <div className="timeline-line">
            <div
              className={`timeline-line-progress ${currentTaskIndex === tasks.length ? 'all-completed' : ''}`}
              style={{ width: getProgressLineWidth() }}
            />
          </div>

          {/* Milestones */}
          {tasks.map((task, index) => (
            <div
              key={index}
              className={`milestone ${getStatusClass(index)} ${selectedTaskIndex === index && getStatusClass(index) !== 'active' ? 'selected' : ''}`}
              onClick={() => handleMilestoneClick(index)}
              style={{ cursor: 'pointer' }}
            >
              <div className="milestone-date">{task.date}</div>
              <div className="milestone-circle">
                {getStatusClass(index) === 'completed' || getStatusClass(index) === 'active' ? '✓' : '✓'}
              </div>
              <div className="milestone-label">
                <div className="milestone-name">{task.shortName}</div>
                <div className="milestone-desc">{task.description}</div>
              </div>

              {/* Note/Flag */}
              {task.note && (
                <>
                  <div className={`milestone-flag ${task.note.type}`} />
                  <div className={`milestone-note ${task.note.type}`}>
                    <div className="note-date">{task.note.date}</div>
                    <div className="note-text">{task.note.text}</div>
                    <div className="note-subtext">{task.note.subtext}</div>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>

        {/* Time Remaining */}
        <div className="time-remaining">
          <span className="time-icon">⏱️</span>
          <span>
            {isRunning
              ? `Progress: ${completedSubtasksCount}/${totalSubtasks} subtasks (${progressPercent.toFixed(1)}%)`
              : 'Left: 5 Months'}
          </span>
        </div>
      </div>

      {/* Subtasks Section */}
      {selectedTaskIndex >= 0 && selectedTaskIndex < tasks.length && (
        <div className="subtasks-container">
          <h3 className="subtasks-header">
            📋 {tasks[selectedTaskIndex].name} - Subtasks
          </h3>

          {tasks[selectedTaskIndex].subtasks.map((subtask, index) => {
            const status = getSubtaskStatus(selectedTaskIndex, index);
            const badge = getStatusBadge(status);

            return (
              <div key={index} className={`subtask-item ${status}`}>
                <div className="subtask-icon">{getStatusIcon(status)}</div>
                <div className="subtask-text">{subtask}</div>
                <div className={`subtask-badge ${badge.class}`}>{badge.text}</div>
              </div>
            );
          })}
        </div>
      )}

      {/* Completion Message */}
      {currentTaskIndex === tasks.length && (
        <div className="completion-message">
          <div className="completion-icon">🎉</div>
          <h2>All Tasks Completed!</h2>
          <p>Project timeline finished successfully</p>
        </div>
      )}
    </div>
  );
};

export default Timeline;

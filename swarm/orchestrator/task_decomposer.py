"""
Task Decomposer - Breaks down complex tasks into manageable subtasks

Analyzes complex tasks and decomposes them into smaller, manageable units
that can be assigned to individual agents or agent groups.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Types of tasks that can be decomposed"""
    DEVELOPMENT = "development"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    ARCHITECTURE = "architecture"


class TaskPriority(Enum):
    """Priority levels for tasks"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class TaskDependency:
    """Represents a dependency between tasks"""
    task_id: str
    dependency_type: str  # "blocks", "requires", "suggests"


@dataclass
class Task:
    """Represents a decomposed task"""
    task_id: str
    title: str
    description: str
    task_type: TaskType
    priority: TaskPriority
    estimated_effort: int  # in story points or hours
    required_capabilities: List[str]
    dependencies: List[TaskDependency]
    acceptance_criteria: List[str]
    metadata: Dict[str, Any]

    def is_ready(self, completed_tasks: set) -> bool:
        """Check if task is ready to be executed"""
        for dep in self.dependencies:
            if dep.dependency_type == "blocks" and dep.task_id not in completed_tasks:
                return False
        return True


@dataclass
class DecompositionResult:
    """Result of task decomposition"""
    original_task: str
    subtasks: List[Task]
    execution_order: List[List[str]]  # List of task batches
    estimated_total_effort: int
    critical_path: List[str]


class TaskDecomposer:
    """
    Decomposes complex tasks into manageable subtasks

    Uses various strategies to break down tasks based on type,
    complexity, and available agent capabilities.
    """

    def __init__(self):
        self.task_counter = 0
        self.decomposition_strategies = {
            TaskType.DEVELOPMENT: self._decompose_development_task,
            TaskType.RESEARCH: self._decompose_research_task,
            TaskType.ANALYSIS: self._decompose_analysis_task,
            TaskType.TESTING: self._decompose_testing_task,
            TaskType.DOCUMENTATION: self._decompose_documentation_task,
            TaskType.ARCHITECTURE: self._decompose_architecture_task,
        }

    async def decompose_task(
        self,
        task_description: str,
        task_type: TaskType,
        context: Optional[Dict[str, Any]] = None
    ) -> DecompositionResult:
        """
        Decompose a complex task into subtasks

        Args:
            task_description: High-level description of the task
            task_type: Type of task being decomposed
            context: Additional context for decomposition

        Returns:
            DecompositionResult with subtasks and execution plan
        """
        logger.info(f"Decomposing {task_type.value} task: {task_description}")

        # Reset task counter for each decomposition
        self.task_counter = 0
        context = context or {}

        # Select appropriate decomposition strategy
        strategy = self.decomposition_strategies.get(task_type)
        if not strategy:
            logger.warning(f"No strategy for task type: {task_type}")
            return self._default_decomposition(task_description, task_type)

        # Execute strategy
        subtasks = await strategy(task_description, context)

        # Build execution order based on dependencies
        execution_order = self._build_execution_order(subtasks)

        # Calculate critical path
        critical_path = self._calculate_critical_path(subtasks, execution_order)

        # Calculate total effort
        total_effort = sum(task.estimated_effort for task in subtasks)

        result = DecompositionResult(
            original_task=task_description,
            subtasks=subtasks,
            execution_order=execution_order,
            estimated_total_effort=total_effort,
            critical_path=critical_path
        )

        logger.info(
            f"Decomposed into {len(subtasks)} subtasks, "
            f"total effort: {total_effort}"
        )

        return result

    async def _decompose_development_task(
        self,
        description: str,
        context: Dict[str, Any]
    ) -> List[Task]:
        """Decompose a development task"""
        subtasks = []

        # Common development task breakdown
        phases = [
            ("design", "Design component architecture", ["architecture", "design"], 3),
            ("implement", "Implement core functionality", ["coding", "development"], 5),
            ("test", "Write and execute tests", ["testing", "qa"], 3),
            ("integrate", "Integrate with existing system", ["integration", "development"], 2),
            ("document", "Write documentation", ["documentation", "writing"], 2),
        ]

        for i, (phase_id, title, capabilities, effort) in enumerate(phases):
            # Generate task ID
            task_id = self._generate_task_id(phase_id)
            
            # Create dependencies from previous task
            dependencies = []
            if i > 0 and subtasks:
                prev_task = subtasks[-1]
                dependencies = [
                    TaskDependency(
                        task_id=prev_task.task_id,
                        dependency_type="blocks"
                    )
                ]
            
            task = Task(
                task_id=task_id,
                title=f"{title}: {description}",
                description=f"{title} phase of: {description}",
                task_type=TaskType.DEVELOPMENT,
                priority=TaskPriority.HIGH,
                estimated_effort=effort,
                required_capabilities=capabilities,
                dependencies=dependencies,
                acceptance_criteria=[f"Complete {title.lower()}"],
                metadata={"phase": phase_id}
            )
            subtasks.append(task)

        return subtasks

    async def _decompose_research_task(
        self,
        description: str,
        context: Dict[str, Any]
    ) -> List[Task]:
        """Decompose a research task"""
        subtasks = []

        research_phases = [
            ("survey", "Literature survey", ["research", "analysis"], 2),
            ("collect", "Data collection", ["research", "data"], 3),
            ("analyze", "Data analysis", ["analysis", "statistics"], 4),
            ("synthesize", "Synthesize findings", ["research", "writing"], 2),
            ("report", "Write research report", ["documentation", "writing"], 3),
        ]

        for i, (phase_id, title, capabilities, effort) in enumerate(research_phases):
            task_id = self._generate_task_id(phase_id)
            
            dependencies = []
            if i > 0 and subtasks:
                prev_task = subtasks[-1]
                dependencies = [
                    TaskDependency(
                        task_id=prev_task.task_id,
                        dependency_type="blocks"
                    )
                ]
            
            task = Task(
                task_id=task_id,
                title=f"{title}: {description}",
                description=f"{title} for research task: {description}",
                task_type=TaskType.RESEARCH,
                priority=TaskPriority.MEDIUM,
                estimated_effort=effort,
                required_capabilities=capabilities,
                dependencies=dependencies,
                acceptance_criteria=[f"Complete {title.lower()}"],
                metadata={"phase": phase_id}
            )
            subtasks.append(task)

        return subtasks

    async def _decompose_analysis_task(
        self,
        description: str,
        context: Dict[str, Any]
    ) -> List[Task]:
        """Decompose an analysis task"""
        subtasks = []

        analysis_phases = [
            ("scope", "Define analysis scope", ["analysis", "planning"], 2),
            ("gather", "Gather data/information", ["research", "data"], 3),
            ("process", "Process and clean data", ["data", "analysis"], 3),
            ("analyze", "Perform analysis", ["analysis", "statistics"], 4),
            ("visualize", "Create visualizations", ["visualization", "data"], 2),
            ("report", "Write analysis report", ["documentation", "writing"], 2),
        ]

        for i, (phase_id, title, capabilities, effort) in enumerate(analysis_phases):
            task_id = self._generate_task_id(phase_id)
            
            dependencies = []
            if i > 0 and subtasks:
                prev_task = subtasks[-1]
                dependencies = [
                    TaskDependency(
                        task_id=prev_task.task_id,
                        dependency_type="blocks"
                    )
                ]
            
            task = Task(
                task_id=task_id,
                title=f"{title}: {description}",
                description=f"{title} for: {description}",
                task_type=TaskType.ANALYSIS,
                priority=TaskPriority.MEDIUM,
                estimated_effort=effort,
                required_capabilities=capabilities,
                dependencies=dependencies,
                acceptance_criteria=[f"Complete {title.lower()}"],
                metadata={"phase": phase_id}
            )
            subtasks.append(task)

        return subtasks

    async def _decompose_testing_task(
        self,
        description: str,
        context: Dict[str, Any]
    ) -> List[Task]:
        """Decompose a testing task"""
        subtasks = []

        testing_phases = [
            ("plan", "Create test plan", ["testing", "planning"], 2),
            ("unit", "Write unit tests", ["testing", "coding"], 3),
            ("integration", "Write integration tests", ["testing", "coding"], 3),
            ("e2e", "Write end-to-end tests", ["testing", "qa"], 2),
            ("execute", "Execute test suite", ["testing", "qa"], 2),
            ("report", "Generate test report", ["documentation", "testing"], 1),
        ]

        for i, (phase_id, title, capabilities, effort) in enumerate(testing_phases):
            task_id = self._generate_task_id(phase_id)
            
            dependencies = []
            if i > 0 and subtasks:
                prev_task = subtasks[-1]
                dependencies = [
                    TaskDependency(
                        task_id=prev_task.task_id,
                        dependency_type="blocks"
                    )
                ]
            
            task = Task(
                task_id=task_id,
                title=f"{title}: {description}",
                description=f"{title} for: {description}",
                task_type=TaskType.TESTING,
                priority=TaskPriority.HIGH,
                estimated_effort=effort,
                required_capabilities=capabilities,
                dependencies=dependencies,
                acceptance_criteria=[f"Complete {title.lower()}"],
                metadata={"phase": phase_id}
            )
            subtasks.append(task)

        return subtasks

    async def _decompose_documentation_task(
        self,
        description: str,
        context: Dict[str, Any]
    ) -> List[Task]:
        """Decompose a documentation task"""
        subtasks = []

        doc_phases = [
            ("outline", "Create documentation outline", ["documentation", "planning"], 1),
            ("draft", "Write first draft", ["documentation", "writing"], 3),
            ("review", "Review and refine", ["documentation", "editing"], 2),
            ("examples", "Add code examples", ["documentation", "coding"], 2),
            ("finalize", "Finalize documentation", ["documentation", "writing"], 1),
        ]

        for i, (phase_id, title, capabilities, effort) in enumerate(doc_phases):
            task_id = self._generate_task_id(phase_id)
            
            dependencies = []
            if i > 0 and subtasks:
                prev_task = subtasks[-1]
                dependencies = [
                    TaskDependency(
                        task_id=prev_task.task_id,
                        dependency_type="blocks"
                    )
                ]
            
            task = Task(
                task_id=task_id,
                title=f"{title}: {description}",
                description=f"{title} for: {description}",
                task_type=TaskType.DOCUMENTATION,
                priority=TaskPriority.MEDIUM,
                estimated_effort=effort,
                required_capabilities=capabilities,
                dependencies=dependencies,
                acceptance_criteria=[f"Complete {title.lower()}"],
                metadata={"phase": phase_id}
            )
            subtasks.append(task)

        return subtasks

    async def _decompose_architecture_task(
        self,
        description: str,
        context: Dict[str, Any]
    ) -> List[Task]:
        """Decompose an architecture task"""
        subtasks = []

        arch_phases = [
            ("requirements", "Gather requirements", ["architecture", "analysis"], 2),
            ("design", "Design system architecture", ["architecture", "design"], 4),
            ("document", "Document architecture", ["documentation", "architecture"], 3),
            ("review", "Architecture review", ["architecture", "review"], 2),
            ("refine", "Refine based on feedback", ["architecture", "design"], 2),
        ]

        for i, (phase_id, title, capabilities, effort) in enumerate(arch_phases):
            task_id = self._generate_task_id(phase_id)
            
            dependencies = []
            if i > 0 and subtasks:
                prev_task = subtasks[-1]
                dependencies = [
                    TaskDependency(
                        task_id=prev_task.task_id,
                        dependency_type="blocks"
                    )
                ]
            
            task = Task(
                task_id=task_id,
                title=f"{title}: {description}",
                description=f"{title} for: {description}",
                task_type=TaskType.ARCHITECTURE,
                priority=TaskPriority.CRITICAL,
                estimated_effort=effort,
                required_capabilities=capabilities,
                dependencies=dependencies,
                acceptance_criteria=[f"Complete {title.lower()}"],
                metadata={"phase": phase_id}
            )
            subtasks.append(task)

        return subtasks

    def _default_decomposition(
        self,
        description: str,
        task_type: TaskType
    ) -> DecompositionResult:
        """Fallback decomposition when no specific strategy exists"""
        task = Task(
            task_id=self._generate_task_id("default"),
            title=description,
            description=description,
            task_type=task_type,
            priority=TaskPriority.MEDIUM,
            estimated_effort=5,
            required_capabilities=["general"],
            dependencies=[],
            acceptance_criteria=["Complete task"],
            metadata={}
        )

        return DecompositionResult(
            original_task=description,
            subtasks=[task],
            execution_order=[[task.task_id]],
            estimated_total_effort=5,
            critical_path=[task.task_id]
        )

    def _build_execution_order(self, subtasks: List[Task]) -> List[List[str]]:
        """Build execution order respecting dependencies"""
        completed = set()
        execution_order = []

        while len(completed) < len(subtasks):
            # Find tasks that can be executed (all dependencies met)
            batch = []
            for task in subtasks:
                if task.task_id not in completed and task.is_ready(completed):
                    batch.append(task.task_id)

            if not batch:
                # Circular dependency or error
                logger.error("Cannot determine execution order - circular dependency?")
                break

            execution_order.append(batch)
            completed.update(batch)

        return execution_order

    def _calculate_critical_path(
        self,
        subtasks: List[Task],
        execution_order: List[List[str]]
    ) -> List[str]:
        """Calculate the critical path through tasks"""
        # Simplified critical path - just take longest sequential path
        path = []
        for batch in execution_order:
            # Find task with highest effort in each batch
            batch_tasks = [t for t in subtasks if t.task_id in batch]
            if batch_tasks:
                longest = max(batch_tasks, key=lambda t: t.estimated_effort)
                path.append(longest.task_id)

        return path

    def _generate_task_id(self, prefix: str) -> str:
        """Generate unique task ID"""
        self.task_counter += 1
        return f"{prefix}_{self.task_counter:04d}"

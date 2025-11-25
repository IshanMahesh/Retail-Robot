class TaskPlannerEvaluator:
    """Evaluate task planning quality"""
    
    def __init__(self):
        self.metrics = []
    
    def evaluate_plan(self, plan: Dict, ground_truth: Dict = None) -> Dict:
        """Evaluate task plan quality"""
        
        metrics = {
            'num_tasks': len(plan['tasks']),
            'critical_tasks': sum(1 for t in plan['tasks'] if t['priority'] == 'CRITICAL'),
            'total_estimated_time': sum(t['estimated_time'] for t in plan['tasks']),
            'has_dependencies': any(t['dependencies'] for t in plan['tasks']),
        }
        
        # Check if critical tasks are prioritized first
        priorities = [t['priority'] for t in plan['tasks']]
        critical_first = all(p != 'CRITICAL' for p in priorities[1:] 
                            if priorities[0] == 'CRITICAL')
        metrics['critical_first'] = critical_first
        
        # Reasoning quality (ask LLM to evaluate)
        if ground_truth:
            metrics['accuracy'] = self._compare_to_ground_truth(plan, ground_truth)
        
        self.metrics.append(metrics)
        return metrics
    
    def _compare_to_ground_truth(self, plan: Dict, ground_truth: Dict) -> float:
        """Compare plan to expert-labeled ground truth"""
        # Simplified: check if top priority tasks match
        plan_critical = {t['type'] for t in plan['tasks'] if t['priority'] == 'CRITICAL'}
        gt_critical = set(ground_truth.get('expected_critical', []))
        
        if not gt_critical:
            return 1.0
        
        overlap = len(plan_critical & gt_critical)
        return overlap / len(gt_critical)
    
    def generate_report(self):
        """Summary statistics"""
        if not self.metrics:
            return "No evaluations yet"
        
        avg_tasks = sum(m['num_tasks'] for m in self.metrics) / len(self.metrics)
        critical_rate = sum(m['critical_first'] for m in self.metrics) / len(self.metrics)
        
        return f"""Task Planning Evaluation Report
        ================================
        Total Evaluations: {len(self.metrics)}
        Avg Tasks per Plan: {avg_tasks:.1f}
        Critical-First Rate: {critical_rate:.1%}
        """

# Test evaluation
evaluator = TaskPlannerEvaluator()

# Run multiple scenarios
for scenario_name in ['spill_emergency', 'busy_store', 'multi_event']:
    detections = create_test_scenario(scenario_name)
    result = planner.plan_tasks(detections, robot_state)
    
    ground_truth = {
        'expected_critical': ['clean_spill'] if 'spill' in scenario_name else []
    }
    
    metrics = evaluator.evaluate_plan(result, ground_truth)
    print(f"\n{scenario_name}: {metrics}")

print(evaluator.generate_report())
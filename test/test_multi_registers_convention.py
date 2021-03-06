# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=unused-import
# pylint: disable=redefined-builtin

"""Test Qiskit's QuantumCircuit class for multiple registers."""

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import compile
from qiskit.quantum_info import state_fidelity, basis_state
from .common import QiskitTestCase
from qiskit_jku_provider import QasmSimulator


class TestCircuitMultiRegs(QiskitTestCase):
    """QuantumCircuit Qasm tests."""

    def test_circuit_multi(self):
        """Test circuit multi regs declared at start.
        """
        qreg0 = QuantumRegister(2, 'q0')
        creg0 = ClassicalRegister(2, 'c0')
        qreg1 = QuantumRegister(2, 'q1')
        creg1 = ClassicalRegister(2, 'c1')
        circ = QuantumCircuit(qreg0, qreg1)
        circ.x(qreg0[1])
        circ.x(qreg1[0])

        meas = QuantumCircuit(qreg0, qreg1, creg0, creg1)
        meas.measure(qreg0, creg0)
        meas.measure(qreg1, creg1)

        qc = circ + meas

        backend_sim = QasmSimulator(silent=True)
        qobj_qc = compile(qc, backend_sim, seed_mapper=34342)
        qobj_circ = compile(circ, backend_sim, seed_mapper=3438)

        result = backend_sim.run(qobj_qc).result()
        counts = result.get_counts(qc)

        target = {'01 10': 1024}

        result = backend_sim.run(qobj_circ).result()
        state = result.get_statevector(circ)

        self.assertEqual(counts, target)
        self.assertAlmostEqual(state_fidelity(basis_state('0110', 4), state), 1.0, places=7)

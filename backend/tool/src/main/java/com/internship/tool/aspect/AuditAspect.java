package com.internship.tool.aspect;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.internship.tool.entity.AuditLog;
import com.internship.tool.repository.AuditLogRepository;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Aspect
@Component
public class AuditAspect {

    @Autowired
    private AuditLogRepository auditLogRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @Around("execution(* com.internship.tool.service.ItemService.create(..))")
    public Object auditCreate(ProceedingJoinPoint joinPoint) throws Throwable {
        Object result = joinPoint.proceed();
        saveLog("Item", "CREATE", null, null, toJson(result));
        return result;
    }

    @Around("execution(* com.internship.tool.service.ItemService.update(..))")
    public Object auditUpdate(ProceedingJoinPoint joinPoint) throws Throwable {
        Object[] args = joinPoint.getArgs();
        Long id = (Long) args[0];
        Object newData = args[1];
        Object result = joinPoint.proceed();
        saveLog("Item", "UPDATE", id, toJson(newData), toJson(result));
        return result;
    }

    @Around("execution(* com.internship.tool.service.ItemService.softDelete(..))")
    public Object auditDelete(ProceedingJoinPoint joinPoint) throws Throwable {
        Object[] args = joinPoint.getArgs();
        Long id = (Long) args[0];
        Object result = joinPoint.proceed();
        saveLog("Item", "DELETE", id, null, null);
        return result;
    }

    private void saveLog(String entity, String operation, Long entityId,
                         String oldValue, String newValue) {
        try {
            String username = "anonymous";
            var auth = SecurityContextHolder.getContext().getAuthentication();
            if (auth != null && auth.isAuthenticated()) {
                username = auth.getName();
            }
            AuditLog log = new AuditLog();
            log.setEntityName(entity);
            log.setOperation(operation);
            log.setEntityId(entityId);
            log.setOldValue(oldValue);
            log.setNewValue(newValue);
            log.setPerformedBy(username);
            log.setPerformedAt(LocalDateTime.now());
            auditLogRepository.save(log);
        } catch (Exception e) {
            System.err.println("Audit log failed: " + e.getMessage());
        }
    }

    private String toJson(Object obj) {
        try {
            return objectMapper.writeValueAsString(obj);
        } catch (Exception e) {
            return obj != null ? obj.toString() : null;
        }
    }
}
